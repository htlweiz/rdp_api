import pytest
from sqlalchemy import create_engine
from rdp.crud import Crud

def test_dummy():
    assert True

# Define a function to initialize Crud
def test_init_crud():
    engine = create_engine('sqlite:///:memory:')
    return Crud(engine)