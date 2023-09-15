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
