import pytest
from sqlalchemy import create_engine
from rdp.crud import Crud

def test_dummy():
    assert True

def test_get_value_types():
    engine = create_engine('sqlite:///:memory:')

    crud = Crud(engine)

    value_types = crud.get_value_types()

    assert isinstance(value_types, list)
    assert all(isinstance(vt, ValueType) for vt in value_types)
