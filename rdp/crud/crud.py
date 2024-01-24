import logging
from typing import List

from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select

from .model import Base, Value, ValueType, Device, Room, Location

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
        return stmt.join(Device.device_name).where(Device.id == self.device_id)

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

class GetDeviceId(Command):
    def __init__(self, device_id: int):
        """Initialize with end time.

        Args:
            end (int): The end time.
        """
        self.device_id = device_id

    def execute(self, stmt: Select) -> Select:
        """Filter the statement by time less than or equal to end.

        Args:
            stmt: The SQL statement to be executed.

        Returns:
            Modified SQL statement filtered by end time.
        """
        return stmt.where(Value.device_id == self.device_id)

class GetRoomID(Command):
    def __init__(self, room_id: int):
        """Initialize with end time.

        Args:
            end (int): The end time.
        """
        self.room_id = room_id

    def execute(self, stmt: Select) -> Select:
        """Filter the statement by time less than or equal to end.

        Args:
            stmt: The SQL statement to be executed.

        Returns:
            Modified SQL statement filtered by end time.
        """
        return stmt.where(Room.room_id == self.room_id)
    
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
                    db_type.type_name = "%d" % value_type_id
                if value_type_unit:
                    db_type.type_unit = value_type_unit
                elif not db_type.type_unit:
                    db_type.type_unit = "UNIT_%d" % value_type_id
                session.add_all([db_type])
                session.commit()
                return db_type
    
    def add_or_update_device(
        self,
        device_id: int = None,
        device_name: str = None,
        device_desc: str = None,
        room_id: int = None
    ) -> None:
        """update or add a device

        Args:
            device_id (int, optional): Device id to be modified (if None a new Device is added), Default to None.
            device_name (str, optional): Device name which should be set or updated. Defaults to None.
            device_desc (str, optional): Device description of measurment wich should be set or updated. Defaults to None.
            room_id (int, optional): Foreign key for Room
        """
        with Session(self._engine) as session:
            stmt = select(Device).where(Device.id == device_id)
            db_device = None
            for type in session.scalars(stmt):
                db_device = type
            if db_device is None:
                db_device = Device(id=device_id)
            if device_name:
                db_device.device_name = device_name
            elif not db_device.device_name:
                db_device.device_name = device_id
            if device_desc:
                db_device.device_desc = device_desc
            elif not db_device.device_desc:
                db_device.device_desc = device_id
            if room_id:
                db_device.room_id = room_id
            elif not db_device.room_id:
                db_device.room_id = room_id
            session.add_all([db_device])
            session.commit()
            return db_device.id

    def add_or_update_room(
        self,
        room_id: int = None,
        room_name: str = None,
        location_id: int = None
    ) -> None:
        """update or add a room

        Args:
            room_id (int, optional): Room id to be modified, Default to None.
            room_name (str, optional): Room name which should be set or updated. Defaults to None.
            location_id (int, optional): Foreign key for Location, Default to None.
        """
        with Session(self._engine) as session:
            stmt = select(Room).where(Room.id == room_id)
            db_room = None
            for type in session.scalars(stmt):
                db_room = type
            if db_room is None:
                db_room = Room(id=room_id)
            if room_name:
                db_room.room_name = room_name
            elif not db_room.room_name:
                db_room.room_name = room_id
            if location_id:
                db_room.location_id = location_id
            elif not db_room.location_id:
                db_room.location_id = location_id
            session.add_all([db_room])
            session.commit()
            return db_room.id
    
    def add_or_update_location(
        self,
        location_id: int = None,
        location: str = None,
    ) -> None:
        """update or add a room

        Args:
            location_id (int, optional): Location id to be modified, Default to None.
            location (str, optional): Location name which should be set or updated. Defaults to None.
        """
        with Session(self._engine) as session:
            stmt = select(Location).where(Location.id == location_id)
            db_loc = None
            for type in session.scalars(stmt):
                db_loc = type
            if db_loc is None:
                db_loc = Location(id=location_id)
            if location:
                db_loc.location = location
            elif not db_loc.location:
                db_loc.location = location_id
            session.add_all([db_loc])
            session.commit()
            return db_loc.id

    def add_value(self, value_time: int, value_type: int, value_value: float, device_id: int) -> None:
        """Add a measurement point to the database.

        Args:
            value_time (int): unix time stamp of the value.
            value_type (int): Valuetype id of the given value. 
            value_value (float): The measurement value as float.
            device_id (int): id from a specific device
        """        
        with Session(self._engine) as session:
            stmt = select(ValueType).where(ValueType.id == value_type)
            db_type = self.add_or_update_value_type(value_type)
            db_value = Value(time=value_time, value=value_value, value_type=db_type, device_id=device_id)

            session.add_all([db_type, db_value])
            try:
                session.commit()
            except IntegrityError:
                logging.error("Integrity")
                raise
    
    def get_room(self, room_id: int) -> Room:
        """Get a special Room

        Args:
            room_id (int): the primary key of the Room

        Returns:
            Room: The Room object
        """
        with Session(self._engine) as session:
            stmt = select(Room).where(Room.id == room_id)
            return session.scalars(stmt).one()
    
    def get_rooms(self) -> List[Room]:
        """Get all configured devices

        Returns:
            List[Room]: List of Room objects. 
        """
        with Session(self._engine) as session:
            stmt = select(Room)
            return session.scalars(stmt).all()
    
    def get_location(self, location_id: int) -> Location:
        """Get a special Location

        Args:
            location_id (int): the primary key of the Location

        Returns:
            Location: The Location object
        """
        with Session(self._engine) as session:
            stmt = select(Location).where(Location.id == location_id)
            return session.scalars(stmt).one()
    
    def get_locations(self) -> List[Location]:
        """Get all configured locations

        Returns:
            List[Location]: List of Location objects. 
        """
        with Session(self._engine) as session:
            stmt = select(Location)
            return session.scalars(stmt).all()

    def get_device(self, device_id: int) -> Device:
        """Get a special Device

        Args:
            device_id (int): the primary key of the Device

        Returns:
            Device: The Device object
        """
        with Session(self._engine) as session:
            stmt = select(Device).where(Device.id == device_id)
            return session.scalars(stmt).one()

    def get_devices(self) -> List[Device]:
        """Get all configured devices

        Returns:
            List[Device]: List of Device objects. 
        """
        with Session(self._engine) as session:
            stmt = select(Device)
            return session.scalars(stmt).all()
        
    def get_value_types(self) -> List[ValueType]:
        """Get all configured value types

        Returns:
            List[ValueType]: List of ValueType objects. 
        """
        with Session(self._engine) as session:
            stmt = select(ValueType)
            return session.scalars(stmt).all()
    
    def get_value_by_device_id(self, device_id: int) -> List[Value]:
        """Get all configured value types

        Returns:
            List[ValueType]: List of ValueType objects. 
        """
        with Session(self._engine) as session:
            stmt = select(Value).where(Value.device_id == device_id)
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
        self, value_type_id: int = None, start: int = None, end: int = None, device_id: int = None, room_id: int = None) -> List[ValueType]:
        """Get Values from database.

        The result can be filtered by the following paramater:

        Args:
            value_type_id (int, optional): If set, only value of this given type will be returned. Defaults to None.
            start (int, optional): If set, only values with a timestamp as least as big as start are returned. Defaults to None.
            end (int, optional): If set, only values with a timestamp as most as big as end are returned. Defaults to None.
            device_id (int): If set, device id will be returned

        Returns:
            List[Value]: List of ValueType objects.
        """
        invoker = Invoker()

        command_configurations = [
            (value_type_id, GetValueTypeId),
            (start, GetTimeStart),
            (end, GetTimeEnd),
            (device_id, GetDeviceId),
            (room_id, GetRoomID)
        ]

        sort_start_commands = {1: TimeAscending, 2: TimeDescending, 3: ValueTypeSorted}

        for param, command_class in command_configurations:
            if param is not None:
                command = command_class(param)
                invoker.add_command(command)

        sort_command = sort_start_commands.get(start)
        if sort_command:
            invoker.add_command(sort_command())
                
        with Session(self._engine) as session:
            stmt = select(Value)
            stmt = invoker.execute_commands(stmt)

            return session.scalars(stmt).all()