from typing import Tuple, Type

from sqlalchemy.orm import Session

from rdp.crud.crud import Crud
from rdp.crud.model import Value


CrudSession = Type[Tuple[Crud, Type[Session]]]

VALUES = [
    (1, 1, 12.2),
    (1, 2, 15.2),
    (2, 2, -17.1232),
    (4, 2, 1.2),
    (5, 2, 6.2),
    (25, 2, 11),
    (54, 2, 14),
    (100, 2, -15.2),
    (99999, 3, -15.2),
    (5, 1, -2),
    (6, 2, 19.3),
]


def test_get_values_all(crud_with_session: CrudSession):
    crud, Session = crud_with_session

    with Session() as session:
        db_values = map(
            lambda value: Value(time=value[0], value_type_id=value[1], value=value[2]),
            VALUES,
        )
        session.add_all(db_values)
        session.commit()

    db_values = list(
        map(
            lambda db_value: (db_value.time, db_value.value_type_id, db_value.value),
            crud.get_values(),
        )
    )

    assert all(db_value in VALUES for db_value in db_values)
    assert all(value in db_values for value in VALUES)


def test_get_values_by_value_type(crud_with_session: CrudSession):
    crud, Session = crud_with_session

    with Session() as session:
        db_values = map(
            lambda value: Value(time=value[0], value_type_id=value[1], value=value[2]),
            VALUES,
        )
        session.add_all(db_values)
        session.commit()

    count = 0
    for i in range(3):
        db_values = crud.get_values(i)
        count += len(db_values)
        assert all(db_value in VALUES for db_value in db_values)

    assert count == len(VALUES)
