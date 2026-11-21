import os

import pytest
from fastapi.testclient import TestClient

from backend.main import app


@pytest.fixture
def client():
    test_url = os.environ.get('TEST_DATABASE_URL', '')
    if not test_url.endswith('/fitness_test') or os.environ.get('DATABASE_URL') != test_url:
        pytest.fail('Run tests with manage.py test using the isolated fitness_test database.')
    with TestClient(app) as c:
        yield c