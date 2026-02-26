# backend/tests/test_smoke.py
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_create_akb_and_get_docs():
    response_create = client.post("/governance/akb", json={"name": "MyTestAKB", "owner": "test_user"})
    assert response_create.status_code == 200
    akb_data = response_create.json()
    akb_id = akb_data["id"]
    assert akb_data["name"] == "MyTestAKB"
    assert akb_data["owner"] == "test_user"
    assert "id" in akb_data

    response_get = client.get(f"/governance/akb/{akb_id}")
    assert response_get.status_code == 200
    assert response_get.json()["id"] == akb_id

    response_docs = client.get("/docs")
    assert response_docs.status_code == 200
