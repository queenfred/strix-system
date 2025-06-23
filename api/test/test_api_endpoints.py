import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "postgres" in response.json()
    assert "s3" in response.json()

def test_create_user():
    payload = {
        "username": "pytest_user",
        "email": "pytest_user@example.com",
        "password": "pytest1234",
        "full_name": "Py Test"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        assert response.json()["username"] == "pytest_user"

def test_get_user():
    response = client.get("/users/pytest_user")
    assert response.status_code == 200
    assert response.json()["username"] == "pytest_user"

def test_create_role():
    payload = {
        "id": 0,
        "name": "pytest_role",
        "description": "Rol para pruebas",
        "permissions": []
    }
    response = client.post("/roles/", json=payload)
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        assert response.json()["name"] == "pytest_role"

def test_get_role():
    response = client.get("/roles/pytest_role")
    assert response.status_code == 200
    assert response.json()["name"] == "pytest_role"
