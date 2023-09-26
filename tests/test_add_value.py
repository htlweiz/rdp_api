import pytest
from typing import Tuple, Type

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from rdp.crud.crud import Crud
from rdp.crud.model import Value


CrudSession = Type[Tuple[Crud, Type[Session]]]


def test_add_value(crud_with_session: CrudSession):
    crud, Session = crud_with_session

    values = [
        (12123, 1, -123),
        (12, 1, -1.2),
        (14, 1, 100),
        (1381, 1, 9999999.99),
        (98315, 1, -999999123.123),
        (1123, 1, 0.00123),
        (12123, 2, -0.012315),
        (12123, 3, 99),
        (12123, 4, 13),
    ]

    for value in values:
        crud.add_value(value[0], value[1], value[2])

    result = None
    with Session() as session:
        query = select(Value)
        result = session.scalars(query).all()

    db_values = list(
        map(lambda value: (value.time, value.value_type_id, value.value), result)
    )

    assert all(db_value in values for db_value in db_values)
    assert all(value in db_values for value in values)


def test_add_value_integrity(crud: Crud):
    unique_values = [
        (1024, 1),
        (9814, 1),
        (5123, 1),
        (1024, 2),
        (112, 2),
        (9999, 2),
        (9999, 3),
        (9999, 4),
        (9999, 5),
    ]

    for value in unique_values:
        crud.add_value(value[0], value[1], 100)

    with pytest.raises(IntegrityError):
        for value in unique_values:
            crud.add_value(value[0], value[1], 100)


def test_add_value_invalid_parameters(crud: Crud):
    values = [
        (None, None, None),
        (None, None, 12.3),
        (None, 15, None),
        (None, 15, -18.2),
        (14, None, None),
        (14, None, 9999),
        (14, 1, None),
    ]

    for value in values:
        with pytest.raises((IntegrityError, TypeError)):
            crud.add_value(value[0], value[1], value[2])
