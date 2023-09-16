import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.exc import NoResultFound, InterfaceError
from sqlalchemy.orm import sessionmaker
from rdp.crud.model import Base, ValueType
from rdp.crud.crud import Crud
from typing import Any


@pytest.fixture(scope="function")
def crud_with_session():
    engine = create_engine("sqlite:///:memory:")

    Session = sessionmaker(bind=engine)

    yield (Crud(engine), Session)

    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def crud():
    engine = create_engine("sqlite:///:memory:")

    yield Crud(engine)

    Base.metadata.drop_all(engine)


def test_add_value_type_missing_parameters(crud: Crud):
    value_types = ["type0", "type1", "temperature", "HUMIDITY_01!"]
    for value_type in value_types:
        with pytest.raises(TypeError):
            crud.add_or_update_value_type(value_type_name=value_type)

    units = ["°C", "%", "UNIT0", "Test"]
    for unit in units:
        with pytest.raises(TypeError):
            crud.add_or_update_value_type(value_type_unit=unit)


def test_add_value_type(crud_with_session: (Crud, Any)):
    crud, Session = crud_with_session

    value_types = [
        {"name": "type0", "unit": "°C"},
        {"name": "type1", "unit": "%"},
        {"name": "temperature", "unit": "UNIT0"},
        {"name": "HUMIDITY_01!", "unit": "Test"},
    ]

    for value_type in value_types:
        crud.add_or_update_value_type(
            value_type_name=value_type["name"], value_type_unit=value_type["unit"]
        )

    db_value_types = None
    with Session() as session:
        query = select(ValueType)

        result = session.scalars(query).all()
        db_value_types = list(
            map(
                lambda value_type: {
                    "name": value_type.type_name,
                    "unit": value_type.type_unit,
                },
                result,
            )
        )

    assert all(db_value_type in value_types for db_value_type in db_value_types)


def test_update_value_type_invalid_ids(crud: Crud):
    invalid_ids = ["foo", "12", "1", "!bar"]

    for id in invalid_ids:
        with pytest.raises(TypeError):
            crud.add_or_update_value_type(id)

    invalid_ids = [[], [1, 2, 3], ["foo"], {}, {"foo": "bar"}]

    for id in invalid_ids:
        with pytest.raises(InterfaceError):
            crud.add_or_update_value_type(id)


def test_add_value_type_default_values(crud_with_session):
    crud, Session = crud_with_session

    ids = [1, 2, 3, 110]
    for id in ids:
        crud.add_or_update_value_type(id)

    result = None
    with Session() as session:
        query = select(ValueType)
        result = session.scalars(query).all()

    for value_type in result:
        assert value_type.type_name == "TYPE_%d" % value_type.id
        assert value_type.type_unit == "UNIT_%d" % value_type.id


def test_update_value_type(crud_with_session):
    crud, Session = crud_with_session

    value_types = {
        1: (None, None),
        2: (None, None),
        10: (None, "K"),
        11: ("foo", "bar"),
        5: ("foo", None),
    }

    for key, value_type in value_types.items():
        crud.add_or_update_value_type(key, value_type[0], value_type[1])

    result = None
    with Session() as session:
        query = select(ValueType)
        result = session.scalars(query).all()

    for db_value_type in result:
        value_type = value_types[db_value_type.id]
        if value_type[0] is None:
            assert db_value_type.type_name == "TYPE_%d" % db_value_type.id
        else:
            assert db_value_type.type_name == value_type[0]
        if value_type[1] is None:
            assert db_value_type.type_unit == "UNIT_%d" % db_value_type.id
        else:
            assert db_value_type.type_unit == value_type[1]

    updated_value_types = {
        1: (None, None),
        2: ("foo", "bar"),
        10: ("Temp", "K"),
        11: ("foo", None),
        5: ("foo", "Bazz"),
    }

    for key, value_type in updated_value_types.items():
        crud.add_or_update_value_type(key, value_type[0], value_type[1])

    with Session() as session:
        query = select(ValueType)
        result = session.scalars(query).all()

    for db_value_type in result:
        value_type = value_types[db_value_type.id]
        updated_value_type = updated_value_types[db_value_type.id]
        if updated_value_type[0] is None:
            name = ""
            if value_type[0] is None:
                name = "TYPE_%d" % db_value_type.id
            else:
                name = value_type[0]

            assert db_value_type.type_name == name
        else:
            assert db_value_type.type_name == updated_value_type[0]
        if updated_value_type[1] is None:
            unit = ""
            if value_type[1] is None:
                unit = "UNIT_%d" % db_value_type.id
            else:
                unit = value_type[1]
            assert db_value_type.type_unit == unit
        else:
            assert db_value_type.type_unit == updated_value_type[1]


def test_get_value_types(crud_with_session: (Crud, Any)):
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


def test_get_value_type_no_id(crud_with_session: (Crud, Any)):
    crud, Session = crud_with_session

    invalid_ids = [1, 12, 22, 999999999, -1, "foo", "Test Test"]
    for id in invalid_ids:
        with pytest.raises(NoResultFound):
            crud.get_value_type(id)

    valid_ids = [1, 12, 22, 100]
    for id in valid_ids:
        pass


def test_get_value_type(crud_with_session: (Crud, Any)):
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
        session.add_all(stored_value_types)
        stored_value_types = list(stored_value_types)

    for stored_value_type in stored_value_types:
        db_value_type = crud.get_value_type(stored_value_type.id)
        assert db_value_type.type_name == stored_value_type.type_name
        assert db_value_type.type_unit == stored_value_type.type_unit
