from fastapi.testclient import TestClient
from rdp.api.main import app

client = TestClient(app)

def test_dummy():
    response = client.get("/")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
