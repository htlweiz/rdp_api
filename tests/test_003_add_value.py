import pytest
from sqlalchemy import create_engine
from rdp.crud import Crud

def test_dummy():
    assert True

def test_add_value():
    engine = create_engine('sqlite:///:memory:')

    crud = Crud(engine)

    crud.add_value(value_time=1632735600, value_type=1, value_value=25.5)

    values = crud.get_values(value_type_id=1)

    assert len(values) == 1
    assert values[0].time == 1632735600
    assert values[0].value == 25.5
