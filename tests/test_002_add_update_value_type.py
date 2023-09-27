import pytest
from sqlalchemy import create_engine
from rdp.crud import Crud

def test_dummy():
    assert True

def test_add_or_update_value_type():
    engine = create_engine('sqlite:///:memory:')

    crud = Crud(engine)

    result = crud.add_or_update_value_type(
        value_type_id=1,
        value_type_name="Test Type",
        value_type_unit="Test Unit"
    )

    value_type = crud.get_value_type(1)

    assert value_type.id == 1
    assert value_type.type_name == "Test Type"
    assert value_type.type_unit == "Test Unit"
