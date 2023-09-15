# test_crud.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from rdp.crud.crud import Crud  # Adjust the import path as needed
from rdp.crud.model import Base

# Define your database URL (use an in-memory SQLite database for simplicity)
DB_URL = "sqlite:///:memory:"

# Initialize the database engine
engine = create_engine(DB_URL)

# Create the database tables
Base.metadata.create_all(engine)

# Create a Pytest fixture to provide a database session
@pytest.fixture(scope="function")
def database_session():
    # Create a new session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Start a transaction
    session.begin()

    yield session

    # Rollback the transaction to leave the database in a clean state
    session.rollback()

    # Close the session
    session.close()

# Add this test to your test_crud.py file

def test_create_engine():
    engine = create_engine("sqlite:///:memory:")  # Use an in-memory SQLite database for testing
    assert engine is not None


# Test case 1: Adding a value type
def test_add_value_type(database_session):
    crud = Crud(engine)
    crud.add_or_update_value_type(value_type_id=1, value_type_name="Test Type", value_type_unit="Test Unit")

    # Retrieve the added value type from the database
    value_type = crud.get_value_type(1)

    # Check if the value type was added successfully
    assert value_type.id == 1
    assert value_type.type_name == "Test Type"
    assert value_type.type_unit == "Test Unit"
# Add this test to your test_crud.py file

def test_get_value_types(database_session):
    crud = Crud(engine)
    crud.add_or_update_value_type(value_type_id=1, value_type_name="Type 1", value_type_unit="Unit 1")
    crud.add_or_update_value_type(value_type_id=2, value_type_name="Type 2", value_type_unit="Unit 2")

    value_types = crud.get_value_types()

    # Check if the value types were retrieved correctly
    assert len(value_types) == 2


# Test case 2: Adding a value
def test_add_value(database_session):
    crud = Crud(engine)
    crud.add_or_update_value_type(value_type_id=1, value_type_name="Test Type", value_type_unit="Test Unit")
    crud.add_value(value_time=123456, value_type=1, value_value=42.0)

    # Retrieve the added value from the database
    values = crud.get_values(value_type_id=1)

    # Check if the value was added successfully
    assert len(values) == 1
    assert values[0].time == 123456
    assert values[0].value == 42.0

# You can add more test cases as needed
# Add this test to your test_crud.py file

def test_add_and_retrieve_value_type(database_session):
    crud = Crud(engine)
    crud.add_or_update_value_type(value_type_id=1, value_type_name="Test Type", value_type_unit="Test Unit")
    
    # Retrieve the added value type
    value_type = crud.get_value_type(1)

    # Check if the value type was added and retrieved correctly
    assert value_type is not None
    assert value_type.id == 1
    assert value_type.type_name == "Test Type"
    assert value_type.type_unit == "Test Unit"

# Add this test to your test_crud.py file


if __name__ == "__main__":
    pytest.main()