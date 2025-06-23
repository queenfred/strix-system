import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_create_permission():
    payload = {
        "id": 0,
        "name": "view_stats",
        "description": "Permite ver estadísticas"
    }
    response = client.post("/permissions/", json=payload)
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        assert response.json()["name"] == "view_stats"

def test_get_permission():
    response = client.get("/permissions/view_stats")
    assert response.status_code == 200
    assert response.json()["name"] == "view_stats"
