"""Start the project's isolated PostgreSQL and run the learning demo."""
import argparse
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
LOCAL = ROOT / '.local'
PG_PORT = 55432

# Handle .exe extension only on Windows
EXE = '.exe' if sys.platform == 'win32' else ''


def postgres_bin():
    configured = os.environ.get('POSTGRES_BIN')
    if configured:
        return Path(configured)
    
    # 1. Try to find pg_ctl in system PATH (works on Linux/macOS/Windows)
    installed = shutil.which('pg_ctl')
    if installed:
        return Path(installed).parent
    
    # 2. Linux/macOS fallback paths
    if sys.platform != 'win32':
        for version in ['18', '17', '16', '15', '14']:
            candidate = Path(f'/usr/lib/postgresql/{version}/bin')
            if (candidate / 'pg_ctl').exists():
                return candidate
    
    # 3. Windows fallback
    if sys.platform == 'win32':
        candidates = sorted(Path('C:/Program Files/PostgreSQL').glob('*/bin/pg_ctl.exe'))
        if candidates:
            return candidates[-1].parent
            
    raise SystemExit('Install PostgreSQL, or set POSTGRES_BIN to its bin directory.')


def execute(command, **kwargs):
    subprocess.run([str(item) for item in command], cwd=ROOT, check=True, **kwargs)


def prepare_database():
    LOCAL.mkdir(exist_ok=True)
    config_path = LOCAL / 'database.json'
    if not config_path.exists():
        config_path.write_text(json.dumps({'password': secrets.token_hex(24)}), encoding='utf-8')
    config = json.loads(config_path.read_text(encoding='utf-8'))
    
    pg = postgres_bin()
    data = LOCAL / 'postgres'
    initialized = (data / 'PG_VERSION').exists() and (data / 'pg_hba.conf').exists()
    
    if data.exists() and not initialized:
        raise SystemExit('Incomplete PostgreSQL setup in .local/postgres. Check its contents before retrying.')
        
    if not initialized:
        password_file = LOCAL / 'init-password.txt'
        password_file.write_text(config['password'], encoding='utf-8')
        try:
            execute([pg / f'initdb{EXE}', '-D', data, '-U', 'fitness',
                     '--auth=scram-sha-256', f'--pwfile={password_file}',
                     '--encoding=UTF8', '--locale=C'])
        finally:
            password_file.unlink(missing_ok=True)
            
    running = subprocess.run(
        [str(pg / f'pg_ctl{EXE}'), '-D', str(data), 'status'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0
    
    if not running:
            pg_opts = f"-p {PG_PORT} -h 127.0.0.1" if sys.platform == 'win32' else f"-p {PG_PORT} -h 127.0.0.1 -c unix_socket_directories='/tmp'"
            execute([str(pg / f'pg_ctl{EXE}'), '-D', str(data), '-l', LOCAL / 'postgres.log',
                     '-o', pg_opts, '-w', 'start'])
                 
    import psycopg
    from psycopg import sql

    with psycopg.connect(
        host='127.0.0.1', port=PG_PORT, user='fitness', password=config['password'],
        dbname='postgres', autocommit=True,
    ) as connection:
        for name in ('fitness_demo', 'fitness_test'):
            if not connection.execute('SELECT 1 FROM pg_database WHERE datname = %s', (name,)).fetchone():
                connection.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(name)))
    return config


def database_url(config, name):
    return f'postgresql+psycopg://fitness:{config["password"]}@127.0.0.1:{PG_PORT}/{name}'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['run', 'migrate', 'test', 'stop-db', 'create-admin'])
    args = parser.parse_args()
    os.chdir(ROOT)
    
    if args.action == 'stop-db':
        execute([str(postgres_bin() / f'pg_ctl{EXE}'), '-D', LOCAL / 'postgres', '-m', 'fast', '-w', 'stop'])
        return
        
    config = prepare_database()
    name = 'fitness_test' if args.action == 'test' else 'fitness_demo'
    os.environ['DATABASE_URL'] = database_url(config, name)
    
    # Run migrations
    execute([sys.executable, '-m', 'alembic', 'upgrade', 'head'])
    
    if args.action == 'test':
        os.environ['TEST_DATABASE_URL'] = os.environ['DATABASE_URL']
        execute([sys.executable, '-m', 'pytest', '-q', 'tests'])
        
    elif args.action == 'create-admin':
        from backend.auth_utils import get_password_hash
        from backend.models import User
        from backend.database import SessionLocal
        
        with SessionLocal() as session:
            existing = session.query(User).filter(User.email == 'admin@example.com').first()
            if existing:
                print("  Admin already exists.")
            else:
                admin = User(
                    email='admin@example.com',
                    password_hash=get_password_hash('Admin123!'),
                    role='admin',
                    is_locked=False
                )
                session.add(admin)
                session.commit()
                print("  Admin created successfully!")
                print("   Email: admin@example.com")
                print("   Password: Admin123!")
                
    elif args.action == 'run':
        if not (ROOT / 'frontend/dist/index.html').exists():
            raise SystemExit('Build frontend first: cd frontend, npm install, npm run build.')
        print('Open http://127.0.0.1:8013 and API docs at http://127.0.0.1:8013/docs', flush=True)
        execute([sys.executable, '-m', 'uvicorn', 'backend.main:app', '--host', '127.0.0.1', '--port', '8013'])


if __name__ == '__main__':
    main()
    