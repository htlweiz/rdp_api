from typing import Tuple, Type

from sqlalchemy.orm import Session

from rdp.crud.crud import Crud
from rdp.crud.model import ValueType


CrudSession = Type[Tuple[Crud, Type[Session]]]


def test_get_value_types(crud_with_session: CrudSession):
    crud, Session = crud_with_session

    value_types = [
        {"name": "type0", "unit": "°C"},
        {"name": "type1", "unit": "%"},
        {"name": "temperature", "unit": "UNIT0"},
        {"name": "HUMIDITY_01!", "unit": "Test"},
    ]

    with Session() as session:
        db_value_types = map(
            lambda value_type: ValueType(
                type_name=value_type["name"], type_unit=value_type["unit"]
            ),
            value_types,
        )
        session.add_all(db_value_types)
        session.commit()

    db_value_types = list(
        map(
            lambda value_type: {
                "name": value_type.type_name,
                "unit": value_type.type_unit,
            },
            crud.get_value_types(),
        )
    )

    assert all(db_value_type in value_types for db_value_type in db_value_types)
    assert all(value_type in db_value_types for value_type in value_types)
