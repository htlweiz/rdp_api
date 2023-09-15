import pytest
from sqlalchemy import create_engine
from rdp.crud.crud import Crud  # Adjust the import path as needed

# Create the database engine (use the same code as in your conftest.py)
DB_URL = "sqlite:///:memory:"
engine = create_engine(DB_URL)

def test_add_value(database_session):
    # Pass the engine, not the session, to the Crud constructor
    crud = Crud(engine)
    crud.add_or_update_value_type(value_type_id=1, value_type_name="Test Type", value_type_unit="Test Unit")
    crud.add_value(value_time=123456, value_type=1, value_value=42.0)

    values = crud.get_values(value_type_id=1)

    assert len(values) == 1
    assert values[0].time == 123456
    assert values[0].value == 42.0
