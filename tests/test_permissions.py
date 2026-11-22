def _register_and_login(client, email, password='Password123!'):
    r = client.post('/api/auth/register', json={'email': email, 'password': password})
    assert r.status_code == 201, f'register failed: {r.status_code} {r.text}'
    token = client.post(
        '/api/auth/login', json={'email': email, 'password': password}
    ).json()['token']
    return {'Authorization': f'Bearer {token}'}


def test_measurements_get_requires_auth(client):
    assert client.get('/api/measurements').status_code == 401


def test_measurements_post_requires_auth(client):
    response = client.post(
        '/api/measurements', json={'weight_kg': 70, 'height_cm': 175}
    )
    assert response.status_code == 401


def test_estimate_requires_auth(client):
    assert client.get('/api/health/estimate').status_code == 401


def test_measurements_scoped_to_owner(client):
    alice = _register_and_login(client, 'alice@example.com')
    bob = _register_and_login(client, 'bob@example.com')
    client.post(
        '/api/measurements', json={'weight_kg': 70, 'height_cm': 175},
        headers=alice,
    )
    client.post(
        '/api/measurements', json={'weight_kg': 80, 'height_cm': 180},
        headers=bob,
    )
    alice_rows = client.get('/api/measurements', headers=alice).json()
    bob_rows = client.get('/api/measurements', headers=bob).json()
    assert len(alice_rows) == 1 and alice_rows[0]['weight_kg'] == 70.0
    assert len(bob_rows) == 1 and bob_rows[0]['weight_kg'] == 80.0


def test_cannot_supply_other_user_id(client):
    alice = _register_and_login(client, 'alice@example.com')
    response = client.post(
        '/api/measurements',
        json={'weight_kg': 70, 'height_cm': 175, 'user_id': 999},
        headers=alice,
    )
    assert response.status_code == 422


def test_estimate_returns_nulls_when_no_measurement(client, member_headers):
    body = client.get('/api/health/estimate', headers=member_headers).json()
    assert body['bmi'] is None
    assert body['tdee'] is None
    assert body['measurement_id'] is None


def test_estimate_returns_missing_fields_when_profile_incomplete(client, member_headers):
    client.post(
        '/api/measurements', json={'weight_kg': 70, 'height_cm': 175},
        headers=member_headers,
    )
    body = client.get('/api/health/estimate', headers=member_headers).json()
    assert body['bmi'] == 22.86
    assert body['tdee'] is None
    assert sorted(body['tdee_missing_fields']) == [
        'activity_level', 'age_years', 'sex_for_equation',
    ]
    assert body['profile_complete'] is False


def test_estimate_returns_tdee_when_profile_complete(client, member_headers):
    client.post(
        '/api/measurements', json={'weight_kg': 70, 'height_cm': 175},
        headers=member_headers,
    )
    client.put(
        '/api/profile',
        json={
            'age_years': 25,
            'sex_for_equation': 'male',
            'activity_level': 'moderately_active',
        },
        headers=member_headers,
    )
    body = client.get('/api/health/estimate', headers=member_headers).json()
    assert body['tdee'] == 2594.31
    assert body['profile_complete'] is True
    assert body['tdee_missing_fields'] == []


def test_estimate_uses_latest_measurement(client, member_headers):
    client.post(
        '/api/measurements', json={'weight_kg': 70, 'height_cm': 175},
        headers=member_headers,
    )
    latest = client.post(
        '/api/measurements', json={'weight_kg': 80, 'height_cm': 175},
        headers=member_headers,
    ).json()
    body = client.get('/api/health/estimate', headers=member_headers).json()
    assert body['measurement_id'] == latest['id']


def test_estimate_scoped_to_own_data(client):
    alice = _register_and_login(client, 'alice@example.com')
    bob = _register_and_login(client, 'bob@example.com')
    client.post(
        '/api/measurements', json={'weight_kg': 70, 'height_cm': 175},
        headers=alice,
    )
    client.post(
        '/api/measurements', json={'weight_kg': 90, 'height_cm': 190},
        headers=bob,
    )
    alice_est = client.get('/api/health/estimate', headers=alice).json()
    bob_est = client.get('/api/health/estimate', headers=bob).json()
    assert alice_est['bmi'] != bob_est['bmi']