import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from rdp.crud.model import Base, ValueType
from rdp.crud.crud import Crud
from typing import Any


@pytest.fixture(scope="function")
def crud_session():
    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    yield (Crud(engine), Session)

    Base.metadata.drop_all(engine)


def test_add_value_type_missing_parameters(crud_session: (Crud, Any)):
    crud, _ = crud_session

    value_types = ["type0", "type1", "temperature", "HUMIDITY_01!"]
    for value_type in value_types:
        with pytest.raises(TypeError):
            crud.add_or_update_value_type(value_type_name=value_type)

    units = ["°C", "%", "UNIT0", "Test"]
    for unit in units:
        with pytest.raises(TypeError):
            crud.add_or_update_value_type(value_type_unit=unit)


def test_add_value_type(crud_session: (Crud, Any)):
    crud, Session = crud_session

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


def test_get_value_types(crud_session: (Crud, Any)):
    crud, Session = crud_session

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


def test_get_value_type_no_id(crud_session: (Crud, Any)):
    crud, Session = crud_session

    wrong_ids = [1, 12, 22, 999999999, -1, "asd", "Test Test"]
    for id in wrong_ids:
        with pytest.raises(NoResultFound):
            crud.get_value_type(id)

    valid_ids = [1, 12, 22, 100]
    for id in valid_ids:
        pass


def test_get_value_type(crud_session: (Crud, Any)):
    crud, Session = crud_session

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
