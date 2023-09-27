import pytest
from sqlalchemy import create_engine
from rdp.crud import Crud

def test_dummy():
    assert True

def test_get_values():
    engine = create_engine('sqlite:///:memory:')

    crud = Crud(engine)

    values = crud.get_values(value_type_id=1, start=1632735600, end=1632736000)

    assert isinstance(values, list)
    assert all(isinstance(v, Value) for v in values)
