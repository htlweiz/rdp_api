from sqlalchemy.orm import Session
from sqlalchemy import select
from .model import Base, Value, ValueType
import logging
from sqlalchemy.exc import IntegrityError, NoResultFound

class SensorCrud:
    def __init__(self, engine):
        self._engine = engine
        self.IntegrityError = IntegrityError 
        self.NoResultFound = NoResultFound

        Base.metadata.create_all(self._engine)

    def add_or_update_value_type(self, value_type_id, value_type_name=None, value_type_unit=None):
        with Session(self._engine) as session:
            stmt = select(ValueType).where(ValueType.id==value_type_id)
            db_type = None
            for type in session.scalars(stmt):
                db_type = type
            if db_type is None:
                db_type = ValueType(id=value_type_id)
            if value_type_name:
                db_type.type_name=value_type_name
            elif not db_type.type_name:
                db_type.type_name="TYPE_%d" % value_type_id
            if value_type_unit:
                db_type.type_unit=value_type_unit
            elif not db_type.type_unit:
                db_type.type_unit="UNIT_%d" % value_type_id
            session.add_all([db_type])
            session.commit()
            return db_type

    def add_value(self, value_time, value_type, value_value):

        with Session(self._engine) as session:
            stmt = select(ValueType).where(ValueType.id==value_type)
            db_type = self.add_or_update_value_type(value_type)
            db_value=Value(
                    time=value_time,
                    value=value_value,
                    value_type=db_type)
            
            session.add_all([db_type, db_value])
            try:
                session.commit()
            except IntegrityError:
                logging.error("Integrity")
                raise 

    def get_value_types(self):
        with Session(self._engine) as session:
            stmt = select(ValueType)
            return session.scalars(stmt).all()

    def get_value_type(self, value_type_id):
        with Session(self._engine) as session:
            stmt = select(ValueType).where(ValueType.id==value_type_id)
            return session.scalars(stmt).one()

    def get_values(self, value_type_id, start=None, end=None):
        with Session(self._engine) as session:
            stmt = select(Value)
            if value_type_id:
                stmt = stmt.join(Value.value_type).where(ValueType.id==value_type_id)
            if start:
                stmt = stmt.where(Value.time >= start)
            if end:
                stmt = stmt.where(Value.time <= end)
            stmt = stmt.order_by(Value.time)
            logging.error(start) 
            logging.error(stmt)

            return session.scalars(stmt).all()

