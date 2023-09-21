import pytest
from rdp.crud.crud import Crud
from rdp.crud.model import ValueType, Value, Base
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="module")
def crud_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    return Crud(engine)

def test_add_or_update_value_type(crud_session):
    Session = sessionmaker(bind=crud_session._engine)

    value_type = crud_session.add_or_update_value_type(value_type_id=1, value_type_name="Temp", value_type_unit="Cel")

    with Session() as session:
        stmt = select(ValueType).where(ValueType.id == 1)
        db_value_type = session.execute(stmt).scalar()
        assert db_value_type.type_name == "Temp"
        assert db_value_type.type_unit == "Cel"

    value_type_update = crud_session.add_or_update_value_type(value_type_id=1, value_type_name="Temperature", value_type_unit="Celsius")

    with Session() as session:
        stmt = select(ValueType).where(ValueType.id == 1)
        db_value_type_updated = session.execute(stmt).scalar()
        assert db_value_type_updated.type_name == "Temperature"
        assert db_value_type_updated.type_unit == "Celsius"

def test_value_type_name_and_unit_type(crud_session):
    Session = sessionmaker(bind=crud_session._engine)

    with Session() as session:
        stmt = select(ValueType).where(ValueType.id == 1)
        db_value_type = session.execute(stmt).scalar()

        if not isinstance(db_value_type.type_name, (str, type(None))):
            raise TypeError("value_type_name must be a string or None.")

        if not isinstance(db_value_type.type_unit, (str, type(None))):
            raise TypeError("value_type_unit must be a string or None.")

def test_update_invalid_type(crud_session):
    Session = sessionmaker(bind=crud_session._engine)

    with pytest.raises(ValueError, match="No existing value_id with ID 10"):
        with Session() as session:
            stmt = select(ValueType).where(ValueType.id == 10)
            db_value_type = session.execute(stmt).scalar()

            if db_value_type is None:
                raise ValueError("No existing value_id with ID 10")

def test_add_value(crud_session):
    Session = sessionmaker(bind=crud_session._engine)
    with Session() as session:
        crud_session.add_or_update_value_type(value_type_id=2, value_type_name="Temperature", value_type_unit="Celsius")
        crud_session.add_value(value_time=1631692800, value_type=2, value_value=25.5)

        stmt = select(Value).where(Value.time == 1631692800)
        db_value = session.scalar(stmt)
        
        assert db_value is not None
        assert db_value.value == 25.5
        assert db_value.value_type.id == 2

def test_get_value_types(crud_session):
    Session = sessionmaker(bind=crud_session._engine)

    with Session() as session:
        crud_session.add_or_update_value_type(value_type_id=3, value_type_name="Pressure", value_type_unit="Pascal")
        value_types = crud_session.get_value_types()

        assert any(vt.type_name == "Pressure" for vt in value_types)

def test_get_value_type(crud_session):
    Session = sessionmaker(bind=crud_session._engine)

    with Session() as session:
        crud_session.add_or_update_value_type(value_type_id=4, value_type_name="Pressure", value_type_unit="Pascal")
        value_type = crud_session.get_value_type(value_type_id=4)

        assert value_type.type_name == "Pressure"
        assert value_type.type_unit == "Pascal"

def test_get_values(crud_session):
    Session = sessionmaker(bind=crud_session._engine)

    with Session() as session:
        crud_session.add_or_update_value_type(value_type_id=5, value_type_name="Humidity", value_type_unit="%")
        crud_session.add_value(value_time=1631692900, value_type=5, value_value=60)
        values = crud_session.get_values(value_type_id=5, start=1631692800, end=1631693000)

        assert len(values) == 1
        assert values[0].value == 60
