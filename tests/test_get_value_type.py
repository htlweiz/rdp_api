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
        ("type0", "°C"),
        ("type1", "%"),
        ("temperature", "UNIT0"),
        ("HUMIDITY_01!", "Test"),
    ]

    with Session() as session:
        db_value_types = map(
            lambda value_type: ValueType(
                type_name=value_type[0], type_unit=value_type[1]
            ),
            value_types,
        )
        session.add_all(db_value_types)
        session.commit()

    for i, value_type in enumerate(value_types):
        db_value_type = crud.get_value_type(i + 1)
        assert db_value_type.type_name == value_type[0]
        assert db_value_type.type_unit == value_type[1]
