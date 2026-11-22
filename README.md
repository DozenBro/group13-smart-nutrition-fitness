Your `README.md` is stale in more ways than just the test count — it still says "12 cases", still describes only measurement endpoints, and still says authentication is "planned" while you've implemented it. Here's the full updated README, ready to replace the file. I've kept the structure and wording style identical so the diff stays small and Đạt can review it quickly.

```markdown
# Smart Nutrition & Fitness

[![Build and test](https://github.com/DozenBro/group13-smart-nutrition-fitness/actions/workflows/ci.yml/badge.svg)](https://github.com/DozenBro/group13-smart-nutrition-fitness/actions/workflows/ci.yml)

A web application for recording body measurements, planning workouts, and suggesting Vietnamese meals. Developed by **Group 13** for the Software Engineering course.

The current version records weight and height, calculates BMI, stores measurement history in PostgreSQL, and provides account and profile APIs with bearer-token sessions. Workouts, TDEE integration, charts, and meals are planned in the sprint specifications.

## Features

- Record weight and height with backend input validation.
- Calculate BMI and display two decimal places.
- View the 30 most recent measurements, newest first.
- Persist data in PostgreSQL and reload history through the API.
- Register, log in, log out, and read/write a profile through a bearer-token API.
- Explore the API using Swagger UI.
- Run automated tests and frontend builds through GitHub Actions.

> The demo uses fictional data. Measurement ownership filtering, admin account management, charts, and TDEE integration remain Sprint 1 milestones. See [SPRINT_1.md](docs/sprints/SPRINT_1.md).

## Tech Stack

| Component | Tools |
| --- | --- |
| Frontend | React, Vite, JavaScript, CSS |
| Backend | Python, FastAPI, Pydantic |
| Database | PostgreSQL |
| ORM and migrations | SQLAlchemy, Alembic |
| Authentication | bcrypt (via passlib), bearer tokens hashed with SHA-256 |
| Testing | pytest, FastAPI TestClient |
| CI | GitHub Actions |

The interface sends JSON requests to FastAPI. The backend validates inputs, performs calculations, enforces session authentication, and reads/writes PostgreSQL through SQLAlchemy. Alembic versions the database schema.

## Prerequisites

The local instructions below target **Windows and PowerShell**, using versions verified in the project. Linux and macOS use the same `manage.py` launcher; PostgreSQL is detected from `/usr/lib/postgresql/*/bin` or `POSTGRES_BIN`.

- Python **3.14**
- Node.js **24** with npm
- PostgreSQL **18**, including `initdb` and `pg_ctl`
- Git

The `manage.py` launcher manages local PostgreSQL on Windows and Linux. CI uses a separate PostgreSQL service on Ubuntu.

## Installation

### 1. Clone the Repository

```powershell
git clone https://github.com/DozenBro/group13-smart-nutrition-fitness.git
cd group13-smart-nutrition-fitness
```

Access to this private repository requires an authorized GitHub account.

### 2. Install Python Dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Install and Build the Frontend

```powershell
cd frontend
npm install
npm run build
cd ..
```

## Running the Application

Run from the repository root.

```powershell
.\.venv\Scripts\python.exe manage.py run
```

Alternatively, open `START.cmd` after installing dependencies and building the frontend.

| URL | Content |
| --- | --- |
| `http://127.0.0.1:8013` | Application interface |
| `http://127.0.0.1:8013/docs` | Swagger UI |

On first startup, the script initializes an isolated PostgreSQL cluster in `.local/postgres`, creates the databases, applies migrations, and starts FastAPI. A random password is stored locally in `.local/database.json` on each machine.

| Local setting | Value |
| --- | --- |
| PostgreSQL address | `127.0.0.1:55432` |
| Application database | `fitness_demo` |
| Test database | `fitness_test` |
| PostgreSQL user | `fitness` |

The script finds PostgreSQL in PATH or the default installation directory. For a different installation, set `POSTGRES_BIN` to its `bin` directory before starting. An example using PostgreSQL 18's default location follows.

```powershell
$env:POSTGRES_BIN = "C:\Program Files\PostgreSQL\18\bin"
.\.venv\Scripts\python.exe manage.py run
```

Stop FastAPI with `Ctrl+C`. Stop the project's PostgreSQL instance using:

```powershell
.\.venv\Scripts\python.exe manage.py stop-db
```

Git ignores `.local`, `.venv`, `frontend/node_modules`, and `frontend/dist`.

## Demo Data (Sprint 1)

Each machine has its own local PostgreSQL. Seed data gives every machine the same starting accounts and measurements; it does not sync data between machines.

After the first `manage.py run` has applied migrations, create the fixed demo accounts:

```powershell
.\.venv\Scripts\python.exe manage.py seed-demo
.\.venv\Scripts\python.exe manage.py create-admin
```

| Role | Email | Password | Notes |
| --- | --- | --- | --- |
| Demo member | `demo@example.com` | `Demo123!` | Owns the pre-existing fictional measurements |
| Member | `member@example.com` | `Member123!` | 3 seeded measurements: 70/175, 71/175, 72/175 |
| Admin | `admin@example.com` | `Admin123!` | Admin role for account management (S1-09) |

Re-running `seed-demo` and `create-admin` is safe; existing accounts are skipped and measurements are only inserted if the member has none. These are fictional local-only accounts. The passwords are documented here for university-project review and must not be reused outside local development. For a deployed environment, supply them at seed time instead of committing them.

## Frontend Development

Keep the backend running through `manage.py run`. In a second terminal, open `frontend` and start Vite.

```powershell
cd frontend
npm run dev
```

Open the local URL printed by Vite, normally `http://127.0.0.1:5173`. Requests to `/api` are proxied to FastAPI on port `8013`.

Vite updates the interface when source files change. To use FastAPI's built frontend on port `8013`, run `npm run build` after frontend changes. Restart the backend after editing Python code.

## API

The measurement and food endpoints are documented below. The account and profile endpoints (register/login/logout/me, profile read/update) are specified in [docs/design/SPRINT_1_API.md](docs/design/SPRINT_1_API.md).

| Method | Endpoint | Auth | Purpose |
| --- | --- | --- | --- |
| `POST` | `/api/measurements` | no¹ | Save a measurement and return BMI |
| `GET` | `/api/measurements` | no¹ | Read measurement history |
| `POST` | `/api/auth/register` | no | Create a Member account |
| `POST` | `/api/auth/login` | no | Issue a bearer token (7-day lifetime) |
| `POST` | `/api/auth/logout` | Bearer | Revoke the current session |
| `GET` | `/api/auth/me` | Bearer | Return the authenticated user |
| `GET` | `/api/profile` | Bearer | Read the authenticated user's profile |
| `PUT` | `/api/profile` | Bearer | Upsert the authenticated user's profile |
| `GET` | `/api/foods` | no | List active foods (Sprint 3 prep) |
| `POST` | `/api/foods` | no | Create a food item (Sprint 3 prep) |
| `DELETE` | `/api/foods/{id}` | no | Deactivate a food item |

¹ Measurement endpoints currently attribute writes to the Demo User. Ownership filtering (S1-06) will require an authenticated session.

Example body for `POST /api/measurements`:

```json
{
  "weight_kg": 70,
  "height_cm": 175
}
```

A valid request returns HTTP `201` with the saved record and BMI `22.86`. Invalid data returns HTTP `422`. The history endpoint defaults to `limit=30` and accepts values from `1` to `100`.

Example for `POST /api/auth/register`:

```json
{ "email": "alice@example.com", "password": "AlicePass123!" }
```

On success (`201`), the response excludes the password and includes only `id`, `email`, `role`, `is_locked`, and `created_at`. Duplicate emails return `409`. Invalid input returns `422`.

Protected endpoints require the header `Authorization: Bearer <token>`, where `<token>` is the `token` value returned by `POST /api/auth/login`. See [docs/design/SPRINT_1_API.md](docs/design/SPRINT_1_API.md) for request/response examples, error codes, and open decisions.

Fields, limits, and acceptance criteria are documented in the [project specification](docs/PROJECT_SPEC.md).

## Testing

```powershell
.\.venv\Scripts\python.exe manage.py test
```

The command uses `fitness_test`, applies migrations, and runs pytest. The current suite has 82 cases covering BMI, TDEE calculation, persistence/retrieval, invalid input, history ordering, food catalog filtering, auth (register/login/logout/current-user), and profile read/update.

The [Build and test](https://github.com/DozenBro/group13-smart-nutrition-fitness/actions/workflows/ci.yml) workflow runs on pushes and pull requests. It initializes PostgreSQL, applies migrations, runs backend tests, and builds the frontend.

## Project Structure

```text
.
├── backend/                 # API, models, auth, database access, and health calculations
├── frontend/
│   ├── src/                 # React interface and CSS
│   ├── package.json
│   └── vite.config.js
├── migrations/              # Schema version history
├── tests/                   # Backend tests
├── docs/
│   ├── PROJECT_SPEC.md      # Shared scope, architecture, and workflow
│   ├── GIT_WORKFLOW.md      # Team Git commands, PRs, review, and merging
│   ├── design/
│   │   ├── SPRINT_1_ERD.md  # Sprint 1 schema and constraints
│   │   └── SPRINT_1_API.md  # Sprint 1 account/profile API contract
│   ├── handover/
│   │   └── S1-07_HEALTH_HANDOVER.md
│   └── sprints/
│       ├── SPRINT_1.md      # Health tracking and accounts
│       ├── SPRINT_2.md      # Workouts and streaks
│       └── SPRINT_3.md      # Meals, integration, and release
├── .github/workflows/ci.yml # Build and test pipeline
├── alembic.ini
├── manage.py                # Local database, migrations, seed, startup, and tests
├── requirements.txt
└── START.cmd
```

## Contributing

Follow the [Git workflow guide](docs/GIT_WORKFLOW.md) for setup, branch commands, commits, pull requests, review, and conflict handling.

1. Take a task and agree on acceptance criteria in its issue.
2. Create a task branch, such as `feature/S1-06-measurement-owner`.
3. Implement the change and run relevant checks.
4. Open a pull request linking the task and describing changes and verification results.
5. Obtain another member's review before merging.

Read the [main specification](docs/PROJECT_SPEC.md) and the relevant sprint specification before starting. Each sprint tracks its stories, acceptance criteria, tasks, verification results, and AI activity log.

## Roadmap

| Stage | Scope |
| --- | --- |
| [Sprint 1](docs/sprints/SPRINT_1.md) | Accounts, authorization, profiles, BMI/TDEE, charts, and account administration |
| [Sprint 2](docs/sprints/SPRINT_2.md) | Exercise catalog, workout plans, completion, and streaks |
| [Sprint 3](docs/sprints/SPRINT_3.md) | Vietnamese foods, meal suggestions, meal completion, and release |

Detailed status and open decisions are tracked in the [project specification](docs/PROJECT_SPEC.md).
