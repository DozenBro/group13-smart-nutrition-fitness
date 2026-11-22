import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

from backend.database import SessionLocal
from backend.main import app
from backend.models import Measurement, Profile, Session as AuthSession, User


@pytest.fixture
def client():
    test_url = os.environ.get('TEST_DATABASE_URL', '')
    if not test_url.endswith('/fitness_test') or os.environ.get('DATABASE_URL') != test_url:
        pytest.fail('Run tests with manage.py test using the isolated fitness_test database.')
    with SessionLocal() as s:
        s.execute(delete(Measurement))
        s.execute(delete(Profile))
        s.execute(delete(AuthSession))
        s.execute(delete(User))
        s.commit()
    with TestClient(app) as c:
        yield c


@pytest.fixture
def member_headers(client):
    email = 'member-fixture@example.com'
    password = 'MemberFixture123!'
    client.post('/api/auth/register', json={'email': email, 'password': password})
    token = client.post(
        '/api/auth/login', json={'email': email, 'password': password}
    ).json()['token']
    return {'Authorization': f'Bearer {token}'}