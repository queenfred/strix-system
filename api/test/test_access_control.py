import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_assign_role_to_user():
    # Asumimos que ya existen usuario con id=1 y rol con id=1
    payload = {
        "user_id": 43,
        "role_id": 67
    }
    response = client.post("/access/assign-role", json=payload)
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        assert response.json()["message"] == "Rol asignado correctamente"

def test_assign_permission_to_role():
    # Asumimos que ya existen permiso con id=1 y rol con id=1
    payload = {
        "role_id": 67,
        "permission_id": 70
    }
    response = client.post("/access/assign-permission", json=payload)
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        assert response.json()["message"] == "Permiso asignado correctamente"
