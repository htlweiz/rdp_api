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

    
# Test case 3: Adding a value
def test_addvalue(database_session):
    crud = Crud(engine)
    crud.add_or_update_value_type(value_type_id=1, value_type_name="Test Type", value_type_unit="Test Unit")
    crud.add_value(value_time=123456, value_type=1, value_value=42.0)

    # Retrieve the added value from the database
    values = crud.get_values(value_type_id=1)

    # Check if the value was added successfully
    assert len(values) == 1
    assert values[0].time == 123456
    assert values[0].value == 42.0
