from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_valid_id():
    response = client.get("/fruit/1")
    assert response.status_code == 200
    assert response.json() == {"fruit": "apple"}
