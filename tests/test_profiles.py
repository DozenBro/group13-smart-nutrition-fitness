def register_and_login(client, email='alice@example.com', password='AlicePass123!'):
    client.post('/api/auth/register', json={'email': email, 'password': password})
    token = client.post(
        '/api/auth/login', json={'email': email, 'password': password}
    ).json()['token']
    return {'Authorization': f'Bearer {token}'}


VALID = {
    'age_years': 25,
    'sex_for_equation': 'male',
    'activity_level': 'moderately_active',
}


def test_profile_get_returns_nulls_when_empty(client):
    headers = register_and_login(client)
    response = client.get('/api/profile', headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body['age_years'] is None
    assert body['sex_for_equation'] is None
    assert body['activity_level'] is None
    assert body['updated_at'] is None


def test_profile_put_creates_then_updates(client):
    headers = register_and_login(client)
    put = client.put('/api/profile', json=VALID, headers=headers)
    assert put.status_code == 200
    assert put.json()['age_years'] == 25
    updated = {**VALID, 'age_years': 30}
    put2 = client.put('/api/profile', json=updated, headers=headers)
    assert put2.status_code == 200
    assert put2.json()['age_years'] == 30
    get = client.get('/api/profile', headers=headers)
    assert get.json()['age_years'] == 30


def test_profile_put_rejects_invalid_age(client):
    headers = register_and_login(client)
    response = client.put(
        '/api/profile',
        json={**VALID, 'age_years': 10},
        headers=headers,
    )
    assert response.status_code == 422


def test_profile_put_rejects_unknown_activity_code(client):
    headers = register_and_login(client)
    response = client.put(
        '/api/profile',
        json={**VALID, 'activity_level': 'superhuman'},
        headers=headers,
    )
    assert response.status_code == 422


def test_profile_put_leaves_existing_unchanged_on_422(client):
    headers = register_and_login(client)
    client.put('/api/profile', json=VALID, headers=headers)
    bad = {**VALID, 'age_years': 10}
    client.put('/api/profile', json=bad, headers=headers)
    get = client.get('/api/profile', headers=headers)
    assert get.json()['age_years'] == 25


def test_profile_scoped_to_authenticated_user(client):
    alice = register_and_login(client, email='alice@example.com')
    bob = register_and_login(client, email='bob@example.com', password='BobPass123!')
    client.put('/api/profile', json=VALID, headers=alice)
    client.put(
        '/api/profile',
        json={**VALID, 'age_years': 40, 'sex_for_equation': 'female'},
        headers=bob,
    )
    assert client.get('/api/profile', headers=alice).json()['age_years'] == 25
    assert client.get('/api/profile', headers=bob).json()['age_years'] == 40