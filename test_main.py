from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
def test_create_user():
    response = client.post('/users/', json={'username': 'testuser'})
    assert response.status_code == 200
    assert response.json()['username'] == 'testuser'


def test_create_todo():
    response = client.post("/todos/", json={"task": "Test Task", "owner_id": 1})
    assert response.status_code == 200
    assert response.json()["task"] == "Test Task"

def test_read_todo():
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json()["task"] == "new task1"