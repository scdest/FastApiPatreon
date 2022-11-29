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
    res_json = response.json()
    assert res_json['name'] == 'Karl'
    assert res_json['email'] == 'test@test.com'

def test_get_created_user(client: TestClient):
    create_response = client.post("/users/", json={'name': 'John', 'email': 'john@test.com'})

    get_response = client.get(f"/users/{create_response.json()['id']}")

    assert get_response.status_code == 200
    get_json = get_response.json()

    assert get_json['name'] == 'John'
    assert get_json['email'] == 'john@test.com'