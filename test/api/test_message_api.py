import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

def test_test_route(client: TestClient):
    response = client.get("/api/test")
    
    assert response.status_code == 200
    assert response.json() == {
        "message": "GET /api/test, API is working",
        "status": "success"
    }

def test_add_message(client: TestClient):
    payload = {"msg": "test message"}
    response = client.post("/api/messages/", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert "msg_id" in data
    assert data["msg"] == "test message"
    
def test_get_messages(client: TestClient):
    payload1 = {"msg": "test message 1"}
    payload2 = {"msg": "test message 2"}
    
    client.post("/api/messages/", json=payload1)
    client.post("/api/messages/", json=payload2)
    
    response = client.get("/api/messages")
    data = response.json()

    assert response.status_code == 200
    assert data[-2]["msg"] == "test message 1"
    assert data[-1]["msg"] == "test message 2"


def test_clear_messages(client: TestClient):
    client.delete("/api/messages")

    payload1 = {"msg": "test message 1"}
    payload2 = {"msg": "test message 2"}

    client.post("/api/messages/", json=payload1)
    client.post("/api/messages/", json=payload2)

    response = client.get("/api/messages")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2

    response = client.delete("/api/messages")
    data = response.json()
    assert response.status_code == 200
    assert data == []

    response = client.get("/api/messages")
    data = response.json()
    assert response.status_code == 200
    assert data == []