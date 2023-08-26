from sqlalchemy.orm import Session
from sqlalchemy import select
from .model import Base, Value, ValueType
import logging
from sqlalchemy.exc import IntegrityError

class SensorCrud:
    def __init__(self, engine):
        self._engine = engine 
        self.IntegrityError = IntegrityError
        Base.metadata.create_all(self._engine)


    def addValue(self, value_time, value_type, value_value):

        with Session(self._engine) as session:
            stmt = select(ValueType).where(ValueType.id==value_type)
            db_type = None
            for type in session.scalars(stmt):
                db_type = type
            if db_type is None:
                db_type = ValueType(
                    id=value_type,
                    type_name="Unset"
                )
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

    
