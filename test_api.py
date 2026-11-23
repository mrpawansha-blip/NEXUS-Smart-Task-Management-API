
import os
os.environ["DATABASE_URL"] = "sqlite:///./test_nexus.db"
os.environ["SECRET_KEY"] = "test-secret-key-only"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_register_login_and_task_crud():
    import uuid
    username = "tester_" + uuid.uuid4().hex[:8]
    email = username + "@example.com"
    registered = client.post("/auth/register", json={
        "username": username, "email": email, "password": "StrongPass123"
    })
    assert registered.status_code == 201

    token_response = client.post("/auth/login", data={
        "username": username, "password": "StrongPass123"
    })
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    created = client.post("/tasks", headers=headers, json={
        "title": "Prepare API demo", "description": "Test CRUD endpoints",
        "status": "pending", "priority": "high"
    })
    assert created.status_code == 201
    task_id = created.json()["id"]

    listed = client.get("/tasks", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) >= 1

    updated = client.patch(f"/tasks/{task_id}", headers=headers, json={"status": "completed"})
    assert updated.status_code == 200
    assert updated.json()["status"] == "completed"

    deleted = client.delete(f"/tasks/{task_id}", headers=headers)
    assert deleted.status_code == 204
