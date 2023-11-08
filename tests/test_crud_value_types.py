from typing import Tuple
import pytest

from sqlalchemy import select
from sqlalchemy.orm import Session

from rdp.crud.crud import Crud
from rdp.crud.model import ValueType

def test_get_value_types_invalid(crud_in_memory: Crud):
    for item in [-13, -1, 0, 1, 5643, 99999999999999, "Test", 3.2]:
        with pytest.raises(crud_in_memory.NoResultFound):
            crud_in_memory.get_value_type(item)

def test_get_value_types_empty(crud_in_memory: Crud):
    result = crud_in_memory.get_value_types()
    assert result == []

def test_get_value_types(crud_session_in_memory: Tuple[Crud, Session]):
    crud_in_memory, session = crud_session_in_memory

    # add value types
    with session() as s:
        s.add(ValueType(id=0, type_name="name", type_unit="TYPE_0"))
        s.add(ValueType(id=1, type_name="weight", type_unit="kg"))
        s.add(ValueType(id=2, type_name="size", type_unit="cm"))
        s.commit()

    result = crud_in_memory.get_value_types()
    assert result != None
    assert len(result) == 3
    for value_type in result:
        assert isinstance(value_type, ValueType)
        assert value_type.id >= 0
        assert value_type.id <= 3
        assert value_type.type_name in ["name", "weight", "size"]

def test_get_value_type(crud_session_in_memory: Tuple[Crud, Session]):
    crud_in_memory, session = crud_session_in_memory

    # add value types
    with session() as s:
        s.add(ValueType(id=0, type_name="name", type_unit="UNIT_0"))
        s.add(ValueType(id=1, type_name="weight", type_unit="kg"))
        s.add(ValueType(id=2, type_name="size", type_unit="cm"))
        s.add(ValueType(id=3, type_name="TYPE_3", type_unit="UNIT_3"))
        s.commit()

    result = crud_in_memory.get_value_type(0)
    assert result != None
    assert isinstance(result, ValueType)
    assert result.id == 0
    assert result.type_name == "name"
    assert result.type_unit == "UNIT_0"
    
    result = crud_in_memory.get_value_type(1)
    assert result != None
    assert isinstance(result, ValueType)
    assert result.id == 1
    assert result.type_name == "weight"
    assert result.type_unit == "kg"

    result = crud_in_memory.get_value_type(2)
    assert result != None
    assert isinstance(result, ValueType)
    assert result.id == 2
    assert result.type_name == "size"
    assert result.type_unit == "cm"

    result = crud_in_memory.get_value_type(3)
    assert result != None
    assert isinstance(result, ValueType)
    assert result.id == 3
    assert result.type_name == "TYPE_3"
    assert result.type_unit == "UNIT_3"

def test_update_value_type_invalid(crud_session_in_memory: Tuple[Crud, Session]):
    crud_in_memory, session = crud_session_in_memory

    # add value types
    with session() as s:
        s.add(ValueType(id=0, type_name="name", type_unit="TYPE_0"))
        s.add(ValueType(id=1, type_name="wwwwww", type_unit="kg"))
        s.add(ValueType(id=2, type_name="size", type_unit="cm"))
        s.commit()

    with pytest.raises(TypeError):
        crud_in_memory.add_or_update_value_type()
    with pytest.raises(TypeError):
        crud_in_memory.add_or_update_value_type("test")
    with pytest.raises(crud_in_memory.IntegrityError):
        crud_in_memory.add_or_update_value_type(2.2)

def test_update_value_types(crud_session_in_memory: Tuple[Crud, Session]):
    crud_in_memory, session = crud_session_in_memory

    # check if database is empty
    result = crud_in_memory.get_value_types()
    assert result == []

    # add value types
    with session() as s:
        s.add(ValueType(id=0, type_name="name", type_unit="TYPE_0"))
        s.add(ValueType(id=1, type_name="wwwwww", type_unit="kg"))
        s.add(ValueType(id=2, type_name="size", type_unit="cm"))
        s.commit()

    # check if value types got added
    with session() as s:
        stmt = select(ValueType)
        result = s.scalars(stmt).all()
        assert result != None
        assert len(result) == 3
        for value_type in result:
            assert isinstance(value_type, ValueType)
            assert value_type.id >= 0 and value_type.id <= 3
            assert value_type.type_name in ["name", "wwwwww", "size"]

    # update value type
    crud_in_memory.add_or_update_value_type(value_type_id=1, value_type_name="weight", value_type_unit="kg")

    # check if value types have changed
    with session() as s:
        stmt = select(ValueType)
        result = s.scalars(stmt).all()
        assert result != None
        assert len(result) == 3
        for value_type in result:
            assert isinstance(value_type, ValueType)
            assert value_type.id >= 0 and value_type.id <= 3
            assert value_type.type_name in ["name", "weight", "size"]
