from fastapi.testclient import TestClient
from dotenv import load_dotenv
load_dotenv()
import pytest

@pytest.fixture(scope='session', autouse=True)
def client(docker_services):
    from app.main import app

    client = TestClient(app)
    yield client

def test_user_does_not_exist(client: TestClient):
    response = client.get("/users/1")
    assert response.status_code == 404
    assert response.json() == {'message': 'user with such id not found'}

def test_user_created(client: TestClient):
    response = client.post("/users/", json={'name': 'Karl', 'email': 'test@test.com'})
    assert response.status_code == 200
    resJson = response.json()
    assert resJson['name'] == 'Karl'
    assert resJson['email'] == 'test@test.com'

def test_get_created_user(client: TestClient):
    createResponse = client.post("/users/", json={'name': 'John', 'email': 'john@test.com'})

    getResponse = client.get(f"/users/{createResponse.json()['id']}")

    assert getResponse.status_code == 200
    getJson = getResponse.json()

    assert getJson['name'] == 'John'
    assert getJson['email'] == 'john@test.com'