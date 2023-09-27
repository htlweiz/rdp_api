import pytest
from sqlalchemy import create_engine
from rdp.crud import Crud

def test_dummy():
    assert True

def test_init_crud():
    engine = create_engine('sqlite:///:memory:')
    assert Crud(engine)