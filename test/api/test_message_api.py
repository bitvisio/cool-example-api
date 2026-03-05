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


def test_get_message_by_id(client: TestClient):
    """Test getting a single message by ID via POST /api/message."""
    client.delete("/api/messages")

    payload = {"msg": "find me"}
    add_response = client.post("/api/messages/", json=payload)
    msg_id = add_response.json()["msg_id"]

    response = client.post("/api/message", json={"msg_id": msg_id})
    data = response.json()

    assert response.status_code == 200
    assert data["msg_id"] == msg_id
    assert data["msg"] == "find me"


def test_get_message_not_found(client: TestClient):
    """Test getting a message with a non-existent ID."""
    client.delete("/api/messages")

    response = client.post("/api/message", json={"msg_id": "non-existent-id"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Message not found"


def test_get_message_missing_msg_id(client: TestClient):
    """Test POST /api/message without msg_id returns 422."""
    response = client.post("/api/message", json={})

    assert response.status_code == 422


def test_get_message_among_multiple(client: TestClient):
    """Test getting the correct message when multiple exist."""
    client.delete("/api/messages")

    client.post("/api/messages/", json={"msg": "first"}).json()
    msg2 = client.post("/api/messages/", json={"msg": "second"}).json()
    client.post("/api/messages/", json={"msg": "third"}).json()

    response = client.post("/api/message", json={"msg_id": msg2["msg_id"]})
    data = response.json()

    assert response.status_code == 200
    assert data["msg_id"] == msg2["msg_id"]
    assert data["msg"] == "second"