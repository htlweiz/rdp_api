import pytest
from sqlalchemy import create_engine
from rdp.crud.crud import Crud  # Adjust the import path as needed

# Create the database engine (use the same code as in your conftest.py)
DB_URL = "sqlite:///:memory:"
engine = create_engine(DB_URL)

def test_add_value_type(database_session):
    # Pass the engine, not the session, to the Crud constructor
    crud = Crud(engine)
    crud.add_or_update_value_type(value_type_id=1, value_type_name="Test Type", value_type_unit="Test Unit")

    value_type = crud.get_value_type(1)

    assert value_type.id == 1
    assert value_type.type_name == "Test Type"
    assert value_type.type_unit == "Test Unit"
