import logging
from typing import List

from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select

from .model import Base, Value, ValueType

class Command(ABC):
    @abstractmethod
    def execute(self, stmt: Select) -> Select:
        """Execute the command on the given statement.

        Args:
            stmt: The SQL statement to be executed.

        Returns:
            Modified SQL statement after executing the command.
        """
        pass

class GetValueTypeId(Command):
    def __init__(self, value_type_id):
        """Initialize with value type ID.

        Args:
            value_type_id (int): The ID of the value type.
        """
        self.value_type_id = value_type_id

    def execute(self, stmt: Select) -> Select:
        """Join with Value type and filter by value type ID.

        Args:
            stmt: The SQL statement to be executed.

        Returns:
            Modified SQL statement after joining and filtering.
        """
        return stmt.join(Value.value_type).where(ValueType.id == self.value_type_id)

class ValueTypeSorted(Command):
    def execute(self, stmt: Select) -> Select:
        """Order the statement by value type ID.

        Args:
            stmt: The SQL statement to be executed.

        Returns:
            Modified SQL statement ordered by value type ID.
        """
        return stmt.order_by(Value.value_type_id)

class GetTimeStart(Command):
    def __init__(self, start: int):
        """Initialize with start time.

        Args:
            start (int): The start time.
        """
        self.start = start

    def execute(self, stmt: Select) -> Select:
        """Filter the statement by time greater than or equal to start.

        Args:
            stmt: The SQL statement to be executed.

        Returns:
            Modified SQL statement filtered by start time.
        """
        return stmt.where(Value.time >= self.start)

class GetTimeEnd(Command):
    def __init__(self, end: int):
        """Initialize with end time.

        Args:
            end (int): The end time.
        """
        self.end = end

    def execute(self, stmt: Select) -> Select:
        """Filter the statement by time less than or equal to end.

        Args:
            stmt: The SQL statement to be executed.

        Returns:
            Modified SQL statement filtered by end time.
        """
        return stmt.where(Value.time <= self.end)

class TimeDescending(Command):
    def execute(self, stmt: Select) -> Select:
        """Order the statement by time in descending order.

        Args:
            stmt: The SQL statement to be executed.

        Returns:
            Modified SQL statement ordered by time in descending order.
        """
        return stmt.order_by(Value.time.desc())

class TimeAscending(Command):
    def execute(self, stmt: Select) -> Select:
        """Order the statement by time in ascending order.

        Args:
            stmt: The SQL statement to be executed.

        Returns:
            Modified SQL statement ordered by time in ascending order.
        """
        return stmt.order_by(Value.time.asc())

class Invoker:
    def __init__(self):
        self.commands = []

    def add_command(self, command) -> None:
        """Add a command to the list of commands.

        Args:
            command (Command): The command to be added.
        """
        self.commands.append(command)

    def execute_commands(self, stmt: Select) -> Select:
        """Execute all commands on the given statement.

        Args:
            stmt: The SQL statement to be executed.

        Returns:
            Modified SQL statement after executing all commands.
        """
        for command in self.commands:
            stmt = command.execute(stmt)
        return stmt
    
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

    def get_values(
        self, value_type_id: int = None, start: int = None, end: int = None) -> List[ValueType]:
        """Get Values from database.

        The result can be filtered by the following paramater:

        Args:
            value_type_id (int, optional): If set, only value of this given type will be returned. Defaults to None.
            start (int, optional): If set, only values with a timestamp as least as big as start are returned. Defaults to None.
            end (int, optional): If set, only values with a timestamp as most as big as end are returned. Defaults to None.

        Returns:
            List[Value]: _description_
        """
        invoker = Invoker()

        start_commands = {
            1: TimeAscending,
            2: TimeDescending,
            3: ValueTypeSorted
        }

        if value_type_id is not None:
            invoker.add_command(GetValueTypeId(value_type_id))
        if start is not None:
            invoker.add_command(GetTimeStart(start))
            command = start_commands.get(start)
            if command:
                invoker.add_command(command())
        if end is not None:
            invoker.add_command(GetTimeEnd(end))
                
        with Session(self._engine) as session:
            stmt = select(Value)
            stmt = invoker.execute_commands(stmt)

            return session.scalars(stmt).all()