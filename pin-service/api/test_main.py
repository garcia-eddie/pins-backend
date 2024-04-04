import os
from fastapi.testclient import TestClient
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

Base.metadata.create_all(bind=engine)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_get_maps():
    response = client.get("/maps/")
    assert response.status_code == 200
