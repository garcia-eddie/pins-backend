from api.tests.conftest import client


def test_create_user(test_db):
    request = {
        "username": "eddie",
        "password": "12345",
        "email": "test@test.com"
    }
    response = client.post("/users", json=request)
    assert response.status_code == 201


def test_get_login_token_user_does_not_exist(test_db):
    response = client.post(
        "/users/token", data={"username": "eddie", "password": "12345"})
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] is not None
    assert data["detail"] == "Incorrect username or password"


def test_get_login_token(test_db):
    request = {
        "username": "eddie",
        "password": "12345",
        "email": "test@test.com"
    }
    response = client.post("/users", json=request)
    assert response.status_code == 201

    response = client.post(
        "/users/token", data={"username": "eddie", "password": "12345"})
    assert response.status_code == 200


def test_get_me(test_db):
    request = {
        "username": "eddie",
        "password": "12345",
        "email": "test@test.com"
    }
    response = client.post("/users", json=request)
    assert response.status_code == 201

    response = client.post(
        "/users/token", data={"username": "eddie", "password": "12345"})
    assert response.status_code == 200

    assert "access_token" in response.json()
    access_token = response.json()["access_token"]
    response = client.get(
        "/users/me", headers={"Authorization": f'bearer {access_token}'}
    )
    assert response.status_code == 200

    assert 'username' in response.json()
    assert response.json()['username'] == 'eddie'
