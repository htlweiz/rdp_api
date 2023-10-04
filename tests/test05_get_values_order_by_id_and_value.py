"""Test the get_values_order_by_id_and_value method from crud."""

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

def test_get_values_order_by_id_and_value_default(crud_instance):
    """Test get_values_order_by_id_and_value with default parameters."""
    values = crud_instance.get_values_order_by_id_and_value()
    assert isinstance(values, list)

def test_get_values_order_by_id_and_value_with_value_type_id(crud_instance):
    """Test get_values_order_by_id_and_value with a specified value_type_id."""
    value_type_id = 1  
    values = crud_instance.get_values_order_by_id_and_value(value_type_id=value_type_id)
    assert isinstance(values, list)

def test_get_values_order_by_id_and_value_with_start_and_end(crud_instance):
    """Test get_values_order_by_id_and_value with specified start and end values."""
    start_value = 1  
    end_value = 10  
    values = crud_instance.get_values_order_by_id_and_value(start=start_value, end=end_value)
    assert isinstance(values, list)

def test_get_values_order_by_id_and_value_with_value_type_id_and_range(crud_instance):
    """Test get_values_order_by_id_and_value with value_type_id and a specified range."""
    value_type_id = 1  
    start_value = 1 
    end_value = 10  
    values = crud_instance.get_values_order_by_id_and_value(value_type_id=value_type_id, start=start_value, end=end_value)
    assert isinstance(values, list)

def test_get_values_order_by_id_and_value_with_invalid_value_type_id(crud_instance):
    """Test get_values_order_by_id_and_value with an invalid value_type_id."""
    invalid_value_type_id = -1  
    values = crud_instance.get_values_order_by_id_and_value(value_type_id=invalid_value_type_id)
    assert isinstance(values, list)
    assert len(values) == 0  


def test_get_values_order_by_id_and_value_with_valid_parameters_and_ordered_results(crud_instance):
    """Test get_values_order_by_id_and_value with valid parameters and ordered results."""
    values = crud_instance.get_values_order_by_id_and_value()
    ids = [value.id for value in values]
    values = [value.value for value in values]

    # Check if the results are ordered by id and value
    assert all(ids[i] <= ids[i + 1] for i in range(len(ids) - 1))
    assert all(values[i] <= values[i + 1] for i in range(len(values) - 1))

def test_get_values_order_by_id_and_value_with_valid_value_type_id_and_ordered_results(crud_instance):
    """Test get_values_order_by_id_and_value with valid value_type_id and ordered results."""
    value_type_id = 1  
    values = crud_instance.get_values_order_by_id_and_value(value_type_id=value_type_id)
    ids = [value.id for value in values]
    values = [value.value for value in values]

    # Check if the results are ordered by id and value
    assert all(ids[i] <= ids[i + 1] for i in range(len(ids) - 1))
    assert all(values[i] <= values[i + 1] for i in range(len(values) - 1))

def test_get_values_order_by_id_and_value_with_valid_start_and_end_parameters_and_ordered_results(crud_instance):
    """Test get_values_order_by_id_and_value with valid start and end parameters and ordered results."""
    start_value = 1
    end_value = 10
    values = crud_instance.get_values_order_by_id_and_value(start=start_value, end=end_value)
    ids = [value.id for value in values]
    values = [value.value for value in values]

    # Check if the results are within the specified range and ordered by id
    assert all(start_value <= ids[i] <= end_value for i in range(len(ids)))
    assert all(ids[i] <= ids[i + 1] for i in range(len(ids) - 1))
    assert all(values[i] <= values[i + 1] for i in range(len(values) - 1))
