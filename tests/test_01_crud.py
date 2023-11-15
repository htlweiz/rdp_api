import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from rdp.crud import Crud

@pytest.fixture(scope="function")
def crud_instance():
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    crud = Crud(engine)
    yield crud
    engine.dispose()

def test_add_value_type(crud_instance):
    value_type = crud_instance.add_or_update_value_type(value_type_name="TestType")
    assert value_type.type_name == "TestType"

def test_add_value(crud_instance):
    crud_instance.add_value(value_time=1, value_type=1, value_value=42.0)
    crud_instance.add_value(value_time=2, value_type=1, value_value=55.0)
    values = crud_instance.get_values()
    assert values[0].value_value == 42.0
    assert values[1].value_value == 55.0

def test_get_value_types(crud_instance):
    value_types = crud_instance.get_value_types()
    assert len(value_types) == 1

def test_get_value_type(crud_instance):
    value_type = crud_instance.get_value_type(value_type_id=1)
    assert value_type is not None

def test_get_values(crud_instance):
    all_values = crud_instance.get_values()
    assert len(all_values) == 2
