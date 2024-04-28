import os
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.database.database import Base, get_db
from api.main import app


TEST_DB_HOST = os.environ.get('DB_HOST')
TEST_DB_NAME = os.environ.get('DB_NAME')
TEST_DB_USER = os.environ.get('DB_USER')
TEST_DB_PASS = os.environ.get('DB_PASS')
TEST_DB_PORT = os.environ.get('DB_PORT')

TEST_DB_URL = f'postgresql://{TEST_DB_USER}:{TEST_DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}'
engine = create_engine(TEST_DB_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# def test_get_map(test_db):
#     response = client.post(
#         "/maps/",
#         json={"name": "boston"}
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert "id" in data
#     id = data["id"]

#     response = client.get(f'/maps/{id}')
#     expected = {
#         "id": id,
#         "name": "boston",
#         "pins": []
#     }
#     assert response.json() == expected


# def test_get_maps(test_db):
#     response = client.post("/maps/", json={"name": "boston"})
#     assert response.status_code == 200
#     data = response.json()
#     assert "id" in data
#     map_id = data["id"]

#     response = client.get('/maps/')
#     data = response.json()
#     expected = [
#         {
#             "id": map_id,
#             "name": "boston",
#             "pins": []
#         }
#     ]
#     assert len(data) == 1
#     assert data == expected


# def test_get_pins(test_db):
#     response = client.post("/maps/", json={"name": "Somerville"})
#     assert response.status_code == 200
#     data = response.json()
#     assert "id" in data
#     map_id = data["id"]

#     request = {
#         "name": "Ogawa",
#         "coordinates": [42.35695407894345, -71.05786815495368],
#         "map_id": map_id
#     }
#     response = client.post("/pins/", json=request)
#     assert response.status_code == 200
#     data = response.json()
#     assert "id" in data
#     pin_id = data["id"]

#     response = client.get('/pins/')
#     data = response.json()
#     expected = [
#         {
#             "id": pin_id,
#             "name": "Ogawa",
#             "coordinates": [42.35695407894345, -71.05786815495368],
#             "map_id": map_id
#         }
#     ]
#     assert len(data) == 1
#     assert data == expected

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
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] is not None
    assert data["detail"] == "Incorrect username"


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
    assert access_token == "eddie"
    response = client.get(
        "/users/me", headers={"Authorization": f'bearer {access_token}'}
    )
    assert response.status_code == 200

    expected = {'disabled': False,
                'email': 'test@test.com',
                'hashed_password': 'HASH12345',
                'id': 1,
                'username': 'eddie'}
    assert response.json() == expected


# def test_me():
#     response = client.post(
#         "/token", data={"username": "eddie", "password": "12345"})
#     assert response.status_code == 200

#     accessToken = response.json()["access_token"]

#     response = client.get("/me", headers={
#         "Authorization": f"Bearer {accessToken}"
#     })
#     assert response.status_code == 200
#     assert response.json() == {
#         "username": "eddie",
#         "email": None,
#         "disabled": False,
#         "hashed_password": "HASH12345"
#     }
