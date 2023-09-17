import pytest
from typing import Tuple, Type

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from rdp.crud.crud import Crud
from rdp.crud.model import ValueType

CrudSession = Type[Tuple[Crud, Type[Session]]]


def test_get_value_type_invalid_id(crud: Crud):
    invalid_ids = [1, 12, 22, 999999999, -1, 12.2, -1.1, -1, "foo", "Test Test"]
    for id in invalid_ids:
        with pytest.raises(NoResultFound):
            crud.get_value_type(id)


def test_get_value_type(crud_with_session: CrudSession):
    crud, Session = crud_with_session

    value_types = [
        {"name": "type0", "unit": "°C"},
        {"name": "type1", "unit": "%"},
        {"name": "temperature", "unit": "UNIT0"},
        {"name": "HUMIDITY_01!", "unit": "Test"},
    ]

    stored_value_types = None
    with Session() as session:
        stored_value_types = map(
            lambda value_type: ValueType(
                type_name=value_type["name"], type_unit=value_type["unit"]
            ),
            value_types,
        )
        stored_value_types = list(stored_value_types)
        session.add_all(stored_value_types)
        session.commit()

    for stored_value_type in stored_value_types:
        db_value_type = crud.get_value_type(stored_value_type.id)
        assert db_value_type.type_name == stored_value_type.type_name
        assert db_value_type.type_unit == stored_value_type.type_unit
