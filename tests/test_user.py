from uuid import uuid4

import pytest


def test_register(test_client):
    data = {
        'username': str(uuid4()),
        'email': str(uuid4()) + '@fojin.tech',
        'password': 'Qwerty134'
    }
    response = test_client.post('/register/', json=data)
    assert response.status_code == 201
    assert response.json() == {'detail': 'Registered'}


def test_register_existing_user(registered_user):
    data = {
        'username': 'testuser',
        'email': 'test@fojin.tech',
        'password': 'Qwerty134'
    }
    response = registered_user.post('/register/', json=data)
    assert response.status_code == 400


def test_register_validation_email(test_client):
    data = {
        'username': str(uuid4()),
        'email': str(uuid4()),
        'password': 'Qwerty134'
    }
    response = test_client.post('/register/', json=data)
    assert response.status_code == 422


@pytest.mark.parametrize('test_data', [
    ({'username': 'testuser', 'password': 'fakepass'}),
    ({'username': 'fakeusername', 'password': 'fakepass'}),
    ({'username': 'fakeusername', 'password': 'Qwerty134'})
])
def test_login_user_with_fake_data(registered_user, test_data):
    response = registered_user.post('/login/', json=test_data)
    assert response.status_code == 401


@pytest.mark.parametrize('test_data', [
    ({'username': 'testuser'}),
    ({'password': 'Qwerty134'})
])
def test_login_validation(registered_user, test_data):
    response = registered_user.post('/login/', json=test_data)
    assert response.status_code == 422


def test_login(registered_user):
    data = {
        'username': 'testuser',
        'password': 'Qwerty134'
    }
    response = registered_user.post('/login/', json=data)
    assert response.status_code == 200
    assert response.json()['access_token'] is not None
    assert response.json()['refresh_token'] is not None


def test_refresh(auth_user):
    token_before_refresh = auth_user.cookies.get('access_token_cookie')
    response = auth_user.post('/refresh/')
    assert response.status_code == 201
    assert response.json()['access_token'] is not None
    assert response.json()['access_token'] != token_before_refresh


def test_get_me(auth_user):
    response = auth_user.get('/me/')
    assert response.status_code == 200
    assert response.json()['username'] == 'testuser'
    assert response.json()['email'] == 'test@fojin.tech'


# def test_logout(auth_user):
#     data = {
#         'username': 'testuser',
#         'password': 'Qwerty134'
#     }
    # response = auth_user.delete('/logout/')
    # assert response.cookies.get() is None
    # print(response.json())
    # assert response.json() == {"msg": "Successfully logout"}

