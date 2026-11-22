def _register_member(client, email='member@example.com', password='MemberPass123!'):
    r = client.post('/api/auth/register', json={'email': email, 'password': password})
    assert r.status_code == 201, r.text
    token = client.post(
        '/api/auth/login', json={'email': email, 'password': password}
    ).json()['token']
    return {'Authorization': f'Bearer {token}'}, r.json()['id']


def test_list_users_requires_auth(client):
    assert client.get('/api/admin/users').status_code == 401


def test_list_users_member_denied(client):
    member, _ = _register_member(client)
    assert client.get('/api/admin/users', headers=member).status_code == 403


def test_list_users_admin_allowed(client, admin_headers):
    _register_member(client)
    r = client.get('/api/admin/users', headers=admin_headers)
    assert r.status_code == 200
    emails = {u['email'] for u in r.json()}
    assert 'admin-fixture@example.com' in emails
    assert 'member@example.com' in emails
    for u in r.json():
        assert 'password_hash' not in u
        assert 'password' not in u


def test_member_cannot_lock(client):
    member, member_id = _register_member(client)
    assert client.post(
        f'/api/admin/users/{member_id}/lock', headers=member
    ).status_code == 403


def test_lock_member_sets_locked(client, admin_headers):
    _, member_id = _register_member(client)
    r = client.post(f'/api/admin/users/{member_id}/lock', headers=admin_headers)
    assert r.status_code == 200
    assert r.json()['is_locked'] is True


def test_lock_member_revokes_existing_sessions(client, admin_headers):
    member, member_id = _register_member(client)
    assert client.get('/api/auth/me', headers=member).status_code == 200
    client.post(f'/api/admin/users/{member_id}/lock', headers=admin_headers)
    assert client.get('/api/auth/me', headers=member).status_code == 401


def test_locked_member_cannot_log_in(client, admin_headers):
    _, member_id = _register_member(client)
    client.post(f'/api/admin/users/{member_id}/lock', headers=admin_headers)
    r = client.post(
        '/api/auth/login',
        json={'email': 'member@example.com', 'password': 'MemberPass123!'},
    )
    assert r.status_code == 403
    assert r.json()['detail'] == 'Account is locked.'


def test_unlock_allows_login_and_preserves_data(client, admin_headers):
    member, member_id = _register_member(client)
    client.post(
        '/api/measurements',
        json={'weight_kg': 70, 'height_cm': 175},
        headers=member,
    )
    client.put(
        '/api/profile',
        json={
            'age_years': 25,
            'sex_for_equation': 'male',
            'activity_level': 'moderately_active',
        },
        headers=member,
    )
    client.post(f'/api/admin/users/{member_id}/lock', headers=admin_headers)
    assert client.get('/api/auth/me', headers=member).status_code == 401

    r = client.post(f'/api/admin/users/{member_id}/unlock', headers=admin_headers)
    assert r.status_code == 200
    assert r.json()['is_locked'] is False

    new_token = client.post(
        '/api/auth/login',
        json={'email': 'member@example.com', 'password': 'MemberPass123!'},
    ).json()['token']
    new_headers = {'Authorization': f'Bearer {new_token}'}

    # Old token is still rejected — unlock does not restore sessions.
    assert client.get('/api/auth/me', headers=member).status_code == 401

    # Data preserved.
    measurements = client.get('/api/measurements', headers=new_headers).json()
    assert len(measurements) == 1
    profile = client.get('/api/profile', headers=new_headers).json()
    assert profile['age_years'] == 25


def test_lock_nonexistent_user(client, admin_headers):
    assert client.post(
        '/api/admin/users/99999/lock', headers=admin_headers
    ).status_code == 404


def test_unlock_nonexistent_user(client, admin_headers):
    assert client.post(
        '/api/admin/users/99999/unlock', headers=admin_headers
    ).status_code == 404