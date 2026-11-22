import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

from backend.auth_utils import get_password_hash
from backend.database import SessionLocal
from backend.main import app
from backend.models import Profile, Session as AuthSession, User


@pytest.fixture
def client():
    test_url = os.environ.get('TEST_DATABASE_URL', '')
    if not test_url.endswith('/fitness_test') or os.environ.get('DATABASE_URL') != test_url:
        pytest.fail('Run tests with manage.py test using the isolated fitness_test database.')
    with SessionLocal() as s:
        s.execute(delete(Profile))
        s.execute(delete(AuthSession))
        s.execute(delete(User))
        s.commit()
        # Recreate the account the S1-03 measurement bridge still depends on.
        # S1-06 will remove this bridge and drop the recreation here.
        s.add(User(
            email='demo@example.com',
            password_hash=get_password_hash('Demo123!'),
            role='member',
            is_locked=False,
        ))
        s.commit()
    with TestClient(app) as c:
        yield c