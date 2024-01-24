"""Test the get_values_order_by_time_and_id method from crud."""


import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from rdp.crud.crud import Crud, Base, Value, ValueType

#Create an in-memory database and set up the SQLAlchemy engine
engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

@pytest.fixture
def crud_instance():
    """Fixture that creates and returns a Crud instance for testing."""
    return Crud(engine)


def test_get_values_default_parameters(crud_instance):
    """Test get_values_order_by_time_and_id with default parameters."""
    values = crud_instance.get_values_order_by_time_and_id()
    assert isinstance(values, list)

def test_get_values_with_value_type_id(crud_instance):
    """Test get_values_order_by_time_and_id with a specified value_type_id."""
    value_type_id = 1 
    values = crud_instance.get_values_order_by_time_and_id(value_type_id=value_type_id)
    assert isinstance(values, list)

def test_get_values_with_invalid_value_type_id(crud_instance):
    """Test get_values_order_by_time_and_id with an invalid value_type_id (negative value)."""
    invalid_value_type_id = -1
    values = crud_instance.get_values_order_by_time_and_id(value_type_id=invalid_value_type_id)
    assert values == [] 

def test_get_values_with_valid_parameters_and_ordered_results(crud_instance):
    """Test get_values_order_by_time_and_id with valid parameters and ordered results."""
    values = crud_instance.get_values_order_by_time_and_id()
    value_type_ids = [value.value_type_id for value in values]
    times = [value.time for value in values]

    # Check if the results are ordered by value_type_id and time
    assert all(value_type_ids[i] <= value_type_ids[i + 1] for i in range(len(value_type_ids) - 1))
    assert all(times[i] <= times[i + 1] for i in range(len(times) - 1))


def test_get_values_with_valid_value_type_id_and_ordered_results(crud_instance):
    """Test get_values_order_by_time_and_id with a valid value_type_id and ordered results."""
    value_type_id = 1  
    values = crud_instance.get_values_order_by_time_and_id(value_type_id=value_type_id)
    value_type_ids = [value.value_type_id for value in values]
    times = [value.time for value in values]

    # Check if the results are ordered by value_type_id and time
    assert all(value_type_ids[i] == value_type_id for i in range(len(value_type_ids)))
    assert all(times[i] <= times[i + 1] for i in range(len(times) - 1))



