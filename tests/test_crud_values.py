import datetime
from typing import Tuple

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import InterfaceError, StatementError

from rdp.crud.crud import Crud
from rdp.crud.model import Value

def test_add_value_invalid(crud_session_in_memory: Tuple[Crud, Session]):
    crud_in_memory, _ = crud_session_in_memory

    with pytest.raises(InterfaceError):
        crud_in_memory.add_value([], 1, 76)

    with pytest.raises(StatementError):
        crud_in_memory.add_value(0, 1, "test")

    with pytest.raises(TypeError):
        crud_in_memory.add_value(0, "test", 76)

def test_add_value(crud_session_in_memory: Tuple[Crud, Session]):
    crud_in_memory, session = crud_session_in_memory

    # add value types
    crud_in_memory.add_or_update_value_type(value_type_id=0, value_type_name="iq", value_type_unit="")
    crud_in_memory.add_or_update_value_type(value_type_id=1, value_type_name="weigth", value_type_unit="kg")
    crud_in_memory.add_or_update_value_type(value_type_id=2, value_type_name="size", value_type_unit="cm")

    crud_in_memory.add_value(int(datetime.datetime(year=2023, month=9, day=26, second=1).timestamp()), 1, 76)
    crud_in_memory.add_value(int(datetime.datetime(year=2023, month=9, day=26, second=1).timestamp()), 2, 180)
    crud_in_memory.add_value(int(datetime.datetime(year=2023, month=9, day=26, second=1).timestamp()), 0, 105)
    crud_in_memory.add_value(int(datetime.datetime(year=2023, month=9, day=26, second=3).timestamp()), 1, 77)
    crud_in_memory.add_value(int(datetime.datetime(year=2023, month=9, day=26, second=3).timestamp()), 2, 181)

    with session() as s:
        stmt = select(Value)
        result = s.scalars(stmt).all()
        assert result != None
        assert len(result) == 5
        for value_type in result:
            assert isinstance(value_type, Value)
            assert value_type.id >= 0 and value_type.id <= 5
            assert value_type.value in [76, 180, 105, 77, 181]
            assert value_type.time in [
                datetime.datetime(year=2023, month=9, day=26, second=1).timestamp(),
                datetime.datetime(year=2023, month=9, day=26, second=3).timestamp()
            ]

def test_get_values(crud_session_in_memory: Tuple[Crud, Session]):
    crud_in_memory, session = crud_session_in_memory

    # add value types
    crud_in_memory.add_or_update_value_type(value_type_id=0, value_type_name="iq", value_type_unit="")
    crud_in_memory.add_or_update_value_type(value_type_id=1, value_type_name="weigth", value_type_unit="kg")
    crud_in_memory.add_or_update_value_type(value_type_id=2, value_type_name="size", value_type_unit="cm")

    # add value types
    with session() as s:
        s.add(Value(time=datetime.datetime(year=2023, month=9, day=26, second=1).timestamp(), value=76, value_type_id=1))
        s.add(Value(time=datetime.datetime(year=2023, month=9, day=26, second=1).timestamp(), value=180, value_type_id=2))
        s.add(Value(time=datetime.datetime(year=2023, month=9, day=26, second=3).timestamp(), value=105, value_type_id=0))
        s.commit()
    
    result = crud_in_memory.get_values()
    assert result != None
    assert len(result) == 3
    for value_type in result:
        assert isinstance(value_type, Value)
        assert value_type.id >= 0 and value_type.id <= 3
        assert value_type.value in [76, 180, 105]
        assert value_type.time in [
            datetime.datetime(year=2023, month=9, day=26, second=1).timestamp(),
            datetime.datetime(year=2023, month=9, day=26, second=3).timestamp()
        ]
