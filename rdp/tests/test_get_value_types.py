import pytest
from sqlalchemy import create_engine
from rdp.crud.crud import Crud  # Adjust the import path as needed

# Create the database engine (use the same code as in your conftest.py)
DB_URL = "sqlite:///:memory:"
engine = create_engine(DB_URL)

def test_get_value_types(database_session):
    # Pass the engine, not the session, to the Crud constructor
    crud = Crud(engine)
    crud.add_or_update_value_type(value_type_id=1, value_type_name="Type 1", value_type_unit="Unit 1")
    crud.add_or_update_value_type(value_type_id=2, value_type_name="Type 2", value_type_unit="Unit 2")

    value_types = crud.get_value_types()

    assert len(value_types) == 2
