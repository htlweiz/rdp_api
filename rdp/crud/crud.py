import logging
from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from .model import Base, Value, ValueType

logging.getLogger().setLevel(logging.INFO)


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
            value_type_id (int, optional):   ValueType id to be modified (if None a new ValueType
                                             is added), Default to None.
            value_type_name (str, optional): Typename wich should be set or updated. Defaults to
                                             None.
            value_type_unit (str, optional): Unit of mesarument wich should be set or updated.
                                             Defaults to None.

        Returns:
            _type_: _description_
        """
        with Session(self._engine) as session:
            statement = select(ValueType).where(ValueType.value_type_id == value_type_id)
            db_type = None
            for single_type in session.scalars(statement):
                db_type = single_type
            if db_type is None:
                db_type = ValueType(value_type_id=value_type_id)
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

    def add_value(self, value_time: int,
                  value_type: int,
                  value_value: float,
                  value_comment: str = "") -> None:
        """Add a measurement point to the database.

        Args:
            value_time (int): unix time stamp of the value.
            value_type (int): Valuetype id of the given value.
            value_value (float): The measurement value as float.
            value_comment (string): An optional comment for a single value
        """
        with Session(self._engine) as session:
            db_type = self.add_or_update_value_type(value_type)
            db_value = Value(time=value_time,
                             value=value_value,
                             value_type=db_type,
                             comment=value_comment)

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
            statement = select(ValueType)
            return session.scalars(statement).all()

    def get_value_type(self, value_type_id: int) -> ValueType:
        """Get a special ValueType

        Args:
            value_type_id (int): the primary key of the ValueType

        Returns:
            ValueType: The ValueType object
        """
        with Session(self._engine) as session:
            statement = select(ValueType).where(ValueType.value_type_id == value_type_id)
            return session.scalars(statement).one()

    def put_value(self, value_id: int,
                  value_type_id: int,
                  value_time: int,
                  value: float,
                  comment: str = ""):
        """Put a single value

        args:
            value(Value): the value to update in the db


        returns:
            Value: The updated value

        raises:
            Curd.NoResultFound
        """
        with Session(self._engine) as session:
            statement = select(Value).where(Value.value_id == value_id)
            temp_value = session.scalar(statement=statement)
            if not temp_value:
                raise NoResultFound("No result for id:%d" % value.value.id)
            temp_value.value = value
            temp_value.value_type_id = value_type_id
            temp_value.time = value_time
            temp_value.comment = comment
            session.add(temp_value)
            session.commit()
            return self.get_value(value_id=value_id)

    def get_value(self, value_id: int) -> Value:
        """Get a single value identified by its id

        args:
            value_id(int):  Value primary id to look for

        Raises:
            Crud.NoResultFound

        Returns (Value):
            the desired value
        """
        with Session(self._engine) as session:
            statement = select(Value).where(Value.value_id == value_id)
            value = session.scalar(statement=statement)
            if not value:
                raise NoResultFound("No result for id:%d" % value_id)
            return value

    def get_values(
        self, value_type_id: int = None, start: int = None, end: int = None
    ) -> List[Value]:
        """Get Values from database.

        The result can be filtered by the following paramater:

        Args:
            value_type_id (int, optional): If set, only value of this given type will be returned.
            Defaults to None.
            start (int, optional): If set, only values with a timestamp as least as big as start
                                   are returned. Defaults to None.
            end (int, optional):   If set, only values with a timestamp as most as big as end are
                                   returned. Defaults to None.

        Returns:
            List[Value]: _description_
        """
        with Session(self._engine) as session:
            statement = select(Value)
            if value_type_id is not None:
                statement = statement.join(Value.value_type).where(
                    ValueType.value_type_id == value_type_id)
            if start is not None:
                statement = statement.where(Value.time >= start)
            if end is not None:
                statement = statement.where(Value.time <= end)
            statement = statement.order_by(Value.time)
            return session.scalars(statement).all()

    def get_min_max_values(
        self, value_type_id: int, start: int = None, end: int = None
    ) -> List[Value]:
        """Get Minimal and Maximal value from database."""

        temp_result = self.get_values(value_type_id=value_type_id, start=start, end=end)

        sorted_result = sorted(temp_result, key=lambda x: x.value)

        min_max = [sorted_result[0], sorted_result[-1]]

        return min_max
