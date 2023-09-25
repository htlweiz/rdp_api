from fastapi.testclient import TestClient
from rdp.api.main import app
from rdp.crud.crud import Crud

client = TestClient(app)

def test_dummy():
    response = client.get("/")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_value_types():
    response = client.get("/type/")
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp != None
    assert len(json_resp) == 3
    for value_type in json_resp:
        for key in value_type.keys():
            assert key in ["id", "type_name", "type_unit"]
