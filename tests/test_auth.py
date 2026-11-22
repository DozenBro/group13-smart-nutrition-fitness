def register(client, email='alice@example.com', password='AlicePass123!'):
    return client.post('/api/auth/register', json={'email': email, 'password': password})


def login(client, email='alice@example.com', password='AlicePass123!'):
    return client.post('/api/auth/login', json={'email': email, 'password': password})


def auth_header(token: str) -> dict[str, str]:
    return {'Authorization': f'Bearer {token}'}


def test_register_creates_member(client):
    response = register(client)
    assert response.status_code == 201
    body = response.json()
    assert body['email'] == 'alice@example.com'
    assert body['role'] == 'member'
    assert body['is_locked'] is False
    assert 'password' not in body
    assert 'password_hash' not in body


def test_register_rejects_duplicate_email(client):
    register(client)
    response = register(client)
    assert response.status_code == 409


def test_register_normalizes_email_case(client):
    register(client, email='Alice@Example.COM')
    response = register(client, email='alice@example.com')
    assert response.status_code == 409


def test_register_rejects_admin_role_attempt(client):
    response = client.post('/api/auth/register', json={
        'email': 'eve@example.com',
        'password': 'EvePass123!',
        'role': 'admin',
    })
    assert response.status_code == 422


def test_register_rejects_short_password(client):
    response = register(client, password='short')
    assert response.status_code == 422


def test_login_returns_token(client):
    register(client)
    response = login(client)
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body['token'], str) and len(body['token']) > 20
    assert body['user']['email'] == 'alice@example.com'


def test_login_wrong_password_returns_401(client):
    register(client)
    response = login(client, password='WrongPass123!')
    assert response.status_code == 401
    assert response.json()['detail'] == 'Invalid credentials.'


def test_login_wrong_email_returns_401_with_same_message(client):
    register(client)
    response = login(client, email='nobody@example.com')
    assert response.status_code == 401
    assert response.json()['detail'] == 'Invalid credentials.'


def test_me_returns_user_with_valid_token(client):
    register(client)
    token = login(client).json()['token']
    response = client.get('/api/auth/me', headers=auth_header(token))
    assert response.status_code == 200
    assert response.json()['email'] == 'alice@example.com'


def test_me_returns_401_without_token(client):
    response = client.get('/api/auth/me')
    assert response.status_code == 401


def test_me_returns_401_with_revoked_token(client):
    register(client)
    token = login(client).json()['token']
    client.post('/api/auth/logout', headers=auth_header(token))
    response = client.get('/api/auth/me', headers=auth_header(token))
    assert response.status_code == 401


def test_logout_revokes_current_session_only(client):
    register(client)
    token_a = login(client).json()['token']
    token_b = login(client).json()['token']
    client.post('/api/auth/logout', headers=auth_header(token_a))
    assert client.get('/api/auth/me', headers=auth_header(token_a)).status_code == 401
    assert client.get('/api/auth/me', headers=auth_header(token_b)).status_code == 200