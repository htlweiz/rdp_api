from typing import Tuple

from sqlalchemy import select
from sqlalchemy.orm import Session

from rdp.crud.crud import Crud
from rdp.crud.model import Value, ValueType

def test_dummy():
    assert True

def test_db_empty(crud_session_in_memory: Tuple[Crud, Session]):
    _, session = crud_session_in_memory

    with session() as s:
        stmt = select(ValueType)
        result = s.scalars(stmt).all()
    assert result == []

    with session() as s:
        stmt = select(Value)
        result = s.scalars(stmt).all()
    assert result == []
