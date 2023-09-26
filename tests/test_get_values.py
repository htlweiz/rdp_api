import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from typing import Tuple, Type

from sqlalchemy.orm import Session

from rdp.crud.crud import Crud
from rdp.crud.model import Base, Value, ValueType, Device


CrudSession = Type[Tuple[Crud, Type[Session]]]

VALUE_TYPES = [("K", "unit1"), ("m", "unit2"), ("s", "unit3")]

DEVICES = ["/dev/test0", "/dev/test1", "/dev/test2", "/dev/test3"]

VALUES = [
    (1, 1, 12.2, 1),
    (1, 1, 12.2, 2),
    (1, 2, 15.2, 1),
    (2, 2, -17.1232, 1),
    (4, 2, 1.2, 2),
    (5, 2, 6.2, 3),
    (25, 2, 11, 1),
    (54, 2, 14, 2),
    (100, 2, -15.2, 3),
    (99999, 3, -15.2, 4),
    (5, 1, -2, 1),
    (6, 2, 19.3, 2),
]


@pytest.fixture(scope="function")
def crud_session_values():
    engine = create_engine("sqlite:///:memory:")

    Session = sessionmaker(bind=engine)

    with Session() as session:
        db_value_types = map(
            lambda value_type: ValueType(
                type_unit=value_type[0], type_name=value_type[1]
            ),
            VALUE_TYPES,
        )
        db_devices = map(lambda device: Device(device=device), DEVICES)
        session.add_all(db_value_types + db_devices)
        session.commit()
        db_values = map(
            lambda value: Value(
                time=value[0], value_type_id=value[1], value=value[2], device=value[3]
            ),
            VALUES,
        )
        session.add_all(db_values)
        session.commit()

    yield (Crud(engine), Session)

    Base.metadata.drop_all(engine)


def test_get_values_all(crud_session_values: CrudSession):
    crud, Session = crud_session_values

    db_values = list(
        map(
            lambda db_value: (
                db_value.time,
                db_value.value_type_id,
                db_value.value,
                db_value.device_id,
            ),
            crud.get_values(),
        )
    )

    assert all(db_value in VALUES for db_value in db_values)
    assert all(value in db_values for value in VALUES)


def test_get_values_by_value_type(crud_session_values: CrudSession):
    crud, Session = crud_session_values

    with Session() as session:
        db_value_types = map(
            lambda value_type: ValueType(
                type_unit=value_type[0], type_name=value_type[1]
            ),
            VALUE_TYPES,
        )
        session.add_all(db_value_types)
        session.commit()
        db_values = map(
            lambda value: Value(time=value[0], value_type_id=value[1], value=value[2]),
            VALUES,
        )
        session.add_all(db_values)
        session.commit()

    count = 0
    for i in range(1, 4):
        db_values = list(
            map(
                lambda db_value: (
                    db_value.time,
                    db_value.value_type_id,
                    db_value.value,
                ),
                crud.get_values(i),
            )
        )
        count += len(db_values)
        assert all(db_value in VALUES for db_value in db_values)

    assert count == len(VALUES)


def test_get_values_by_start(crud_session_values: CrudSession):
    crud, Session = crud_session_values

    with Session() as session:
        db_value_types = map(
            lambda value_type: ValueType(
                type_unit=value_type[0], type_name=value_type[1]
            ),
            VALUE_TYPES,
        )
        session.add_all(db_value_types)
        session.commit()
        db_values = map(
            lambda value: Value(time=value[0], value_type_id=value[1], value=value[2]),
            VALUES,
        )
        session.add_all(db_values)
        session.commit()

    times = [1, 2, 5, 100]
    for time in times:
        filtered_values = [value for value in VALUES if value[0] >= time]
        db_values = list(
            map(
                lambda db_value: (
                    db_value.time,
                    db_value.value_type_id,
                    db_value.value,
                ),
                crud.get_values(start=time),
            )
        )

        assert all(db_value in filtered_values for db_value in db_values)
        assert all(value in db_values for value in filtered_values)


def test_get_values_by_end(crud_session_values: CrudSession):
    crud, Session = crud_session_values

    with Session() as session:
        db_value_types = map(
            lambda value_type: ValueType(
                type_unit=value_type[0], type_name=value_type[1]
            ),
            VALUE_TYPES,
        )
        session.add_all(db_value_types)
        session.commit()
        db_values = map(
            lambda value: Value(time=value[0], value_type_id=value[1], value=value[2]),
            VALUES,
        )
        session.add_all(db_values)
        session.commit()

    times = [1, 2, 5, 99, 100, 101, 9999, 999999]
    for time in times:
        filtered_values = [value for value in VALUES if value[0] <= time]
        db_values = list(
            map(
                lambda db_value: (
                    db_value.time,
                    db_value.value_type_id,
                    db_value.value,
                ),
                crud.get_values(end=time),
            )
        )

        assert all(db_value in filtered_values for db_value in db_values)
        assert all(value in db_values for value in filtered_values)


def test_get_values_all_filters(crud_session_values: CrudSession):
    crud, Session = crud_session_values

    with Session() as session:
        db_value_types = map(
            lambda value_type: ValueType(
                type_unit=value_type[0], type_name=value_type[1]
            ),
            VALUE_TYPES,
        )
        session.add_all(db_value_types)
        session.commit()
        db_values = map(
            lambda value: Value(time=value[0], value_type_id=value[1], value=value[2]),
            VALUES,
        )
        session.add_all(db_values)
        session.commit()

    type_ids = [1, 2, 3]
    times = [1, 2, 5, 99, 100, 101, 9999, 1000000]
    for start in times:
        for end in times:
            for type_id in type_ids:
                filtered_values = [
                    value
                    for value in VALUES
                    if value[0] >= start and value[0] <= end and value[1] == type_id
                ]
                db_values = list(
                    map(
                        lambda db_value: (
                            db_value.time,
                            db_value.value_type_id,
                            db_value.value,
                        ),
                        crud.get_values(start=start, end=end, value_type_id=type_id),
                    )
                )

                assert all(db_value in filtered_values for db_value in db_values)
                assert all(value in db_values for value in filtered_values)
