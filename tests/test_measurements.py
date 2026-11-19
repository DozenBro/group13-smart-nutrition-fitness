import os
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from backend.health import calculate_bmi


@pytest.fixture
def client():
    test_url = os.environ.get('TEST_DATABASE_URL', '')
    if not test_url.endswith('/fitness_test') or os.environ.get('DATABASE_URL') != test_url:
        pytest.fail('Run tests with manage.py test using the isolated fitness_test database.')
    from backend.main import app
    from backend.database import get_session
    from sqlalchemy.orm import Session

    engine = create_engine(test_url)
    with engine.connect() as connection:
        transaction = connection.begin()
        session = Session(bind=connection, join_transaction_mode='create_savepoint')
        # Reads use exactly this test transaction; the fixture rolls it all back.
        def test_session():
            yield session
        app.dependency_overrides[get_session] = test_session
        try:
            with TestClient(app) as test_client:
                yield test_client
        finally:
            app.dependency_overrides.clear()
            session.close()
            transaction.rollback()
    engine.dispose()


def test_bmi_known_example():
    assert calculate_bmi(Decimal('70'), Decimal('175')) == Decimal('22.86')


def test_save_then_read(client):
    response = client.post('/api/measurements', json={'weight_kg': 70, 'height_cm': 175})
    assert response.status_code == 201
    record = response.json()
    assert record['bmi'] == 22.86
    assert record['created_at'].endswith('Z') or '+' in record['created_at']
    history = client.get('/api/measurements').json()
    assert history[0] == record


@pytest.mark.parametrize('data', [
    {'weight_kg': 70, 'height_cm': 0},
    {'weight_kg': 0, 'height_cm': 175},
    {'weight_kg': -1, 'height_cm': 175},
    {'weight_kg': 70, 'height_cm': 251},
    {'weight_kg': 501, 'height_cm': 175},
    {'weight_kg': 70.123, 'height_cm': 175},
    {'weight_kg': 70},
    {'weight_kg': 'NaN', 'height_cm': 175},
    {'weight_kg': 70, 'height_cm': 175, 'unexpected': 'value'},
])
def test_invalid_input_does_not_save(client, data):
    before = client.get('/api/measurements').json()
    assert client.post('/api/measurements', json=data).status_code == 422
    assert client.get('/api/measurements').json() == before


def test_newest_first_and_limit(client):
    first = client.post('/api/measurements', json={'weight_kg': 70, 'height_cm': 175}).json()
    second = client.post('/api/measurements', json={'weight_kg': 71, 'height_cm': 175}).json()
    assert client.get('/api/measurements?limit=1').json() == [second]
    assert second['id'] > first['id']
    assert client.get('/api/measurements?limit=0').status_code == 422
