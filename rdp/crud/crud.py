"""Crud Module. """

import logging
from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from .model import Base, Value, ValueType


class Crud:
    def __init__(self, engine):
        self._engine = engine
        self.IntegrityError = IntegrityError
        self.NoResultFound = NoResultFound

        Base.metadata.create_all(self._engine)

    def add_or_update_value_type(
        self,
        value_type_id: int = None,
        value_type_name: str = None,
        value_type_unit: str = None,
    ) -> None:
        """update or add a value type

        Args:
            value_type_id (int, optional): ValueType id to be modified (if None a new ValueType is added), Default to None.
            value_type_name (str, optional): Typename wich should be set or updated. Defaults to None.
            value_type_unit (str, optional): Unit of mesarument wich should be set or updated. Defaults to None.

        Returns:
            _type_: _description_
        """
        with Session(self._engine) as session:
            stmt = select(ValueType).where(ValueType.id == value_type_id)
            db_type = None
            for type in session.scalars(stmt):
                db_type = type
            if db_type is None:
                db_type = ValueType(id=value_type_id)
            if value_type_name:
                db_type.type_name = value_type_name
            elif not db_type.type_name:
                db_type.type_name = "TYPE_%d" % value_type_id
            if value_type_unit:
                db_type.type_unit = value_type_unit
            elif not db_type.type_unit:
                db_type.type_unit = "UNIT_%d" % value_type_id
            session.add_all([db_type])
            session.commit()
            return db_type

    def add_value(self, value_time: int, value_type: int, value_value: float) -> None:
        """Add a measurement point to the database.

        Args:
            value_time (int): unix time stamp of the value.
            value_type (int): Valuetype id of the given value. 
            value_value (float): The measurement value as float.
        """        
        with Session(self._engine) as session:
            stmt = select(ValueType).where(ValueType.id == value_type)
            db_type = self.add_or_update_value_type(value_type)
            db_value = Value(time=value_time, value=value_value, value_type=db_type)

            session.add_all([db_type, db_value])
            try:
                session.commit()
            except IntegrityError:
                logging.error("Integrity")
                raise

    def get_value_types(self) -> List[ValueType]:
        """Get all configured value types

        Returns:
            List[ValueType]: List of ValueType objects. 
        """
        with Session(self._engine) as session:
            stmt = select(ValueType)
            return session.scalars(stmt).all()

    def get_value_type(self, value_type_id: int) -> ValueType:
        """Get a special ValueType

        Args:
            value_type_id (int): the primary key of the ValueType

        Returns:
            ValueType: The ValueType object
        """
        with Session(self._engine) as session:
            stmt = select(ValueType).where(ValueType.id == value_type_id)
            return session.scalars(stmt).one()

    def get_values_order_by_time_and_id(self, value_type_id: int = None, start: int = None, end: int = None) -> List[Value]:
        """
        Retrieve values from the database, ordered by value_type_id and time.
        
        Args:
            value_type_id (int, optional): The ID of the value type to filter by.
            start (int, optional): The start value for filtering by type_id.
            end (int, optional): The end value for filtering by type_id.
            
        Returns:
            List[Value]: A list of Value objects retrieved from the database, ordered by value_type_id and time.
        """
        
        with Session(self._engine) as session:
            query = session.query(Value).join(Value.value_type)

            if value_type_id is not None:
                query = query.filter(ValueType.id == value_type_id)

            if start is not None:
                query = query.filter(Value.type_id >= start)

            if end is not None:
                query = query.filter(Value.type_id <= end)

            # Sort in the desired order: value_type_id, time
            query = query.order_by(Value.value_type_id, Value.time)

            values = query.all()
            return values


    def get_values_order_by_id_and_value(self, value_type_id: int = None, start: int = None, end: int = None) -> List[Value]:
        """
        Retrieve a list of Value objects ordered by value_type_id and value.

        Args:
            value_type_id (int, optional): The ID of the value type to filter by. Defaults to None.
            start (int, optional): The minimum value_type_id to filter by. Defaults to None.
            end (int, optional): The maximum value_type_id to filter by. Defaults to None.

        Returns:
            List[Value]: A list of Value objects ordered by value_type_id and value.
        """
        with Session(self._engine) as session:
            query = session.query(Value).join(Value.value_type)

            if value_type_id is not None:
                query = query.filter(ValueType.id == value_type_id)

            if start is not None:
                query = query.filter(Value.value_type_id >= start)

            if end is not None:
                query = query.filter(Value.value_type_id <= end)

            # Sort in the desired order: value_type_id, value
            query = query.order_by(Value.value_type_id, Value.value)

            values = query.all()
            return values

