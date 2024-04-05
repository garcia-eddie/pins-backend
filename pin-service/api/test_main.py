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


def test_get_map(test_db):
    response = client.post(
        "/maps/",
        json={"name": "boston"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    id = data["id"]

    response = client.get(f'/maps/{id}')
    expected = {
        "id": id,
        "name": "boston",
        "pins": []
    }
    assert response.json() == expected


def test_get_maps(test_db):
    response = client.post("/maps/", json={"name": "boston"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    map_id = data["id"]

    response = client.get('/maps/')
    data = response.json()
    expected = [
        {
            "id": map_id,
            "name": "boston",
            "pins": []
        }
    ]
    assert len(data) == 1
    assert data == expected
