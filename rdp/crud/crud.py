import logging
from typing import List

from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from .model import Base, Value, ValueType, Device, Room, RoomGroup


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

    def add_value(
            self,
            value_time: int,
            value_type: int,
            value_value: float,
            device_id: int) -> None:
        """Add a measurement point to the database.

        Args:
            value_time (int): unix time stamp of the value.
            value_type (int): Valuetype id of the given value. 
            value_value (float): The measurement value as float.
            device_id (int): The id of the device.
        """
        with Session(self._engine) as session:
            db_value = Value(time=value_time, value=value_value, value_type_id=value_type, device_id=device_id)
            session.add_all([db_value])
            session.commit()

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
        self, value_type_id: int = None, start: int = None, end: int = None
    ) -> List[Value]:
        """Get Values from database.

        The result can be filtered by the following paramater:

        Args:
            value_type_id (int, optional): If set, only value of this given type will be returned. Defaults to None.
            start (int, optional): If set, only values with a timestamp as least as big as start are returned. Defaults to None.
            end (int, optional): If set, only values with a timestamp as most as big as end are returned. Defaults to None.

        Returns:
            List[Value]: _description_
        """
        with Session(self._engine) as session:
            stmt = select(Value)
            if value_type_id is not None:
                stmt = stmt.join(Value.value_type).where(ValueType.id == value_type_id)
            if start is not None:
                stmt = stmt.where(Value.time >= start)
            if end is not None:
                stmt = stmt.where(Value.time <= end)
            stmt = stmt.order_by(Value.time)
            logging.error(start)
            logging.error(stmt)

            return session.scalars(stmt).all()

    def get_device(self, device_id=None) -> Device:
        """Get all configured devices

        Returns:
            List[Device]: List of Device objects. 
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

    def add_or_update_device(
        self,
        device_id: int = None,
        device_name: str = None,
        room_id: int = None
    ) -> None:
        """update or add a device

        Args:
            device_id (int, optional): Device id to be modified (if None a new Device is added), Default to None.
            device_name (str, optional): Devicename wich should be set or updated. Defaults to None.

        Returns:
            _type_: _description_
        """
        with Session(self._engine) as session:
            stmt = select(Device).where(Device.id == device_id)
            db_device = None
            for device in session.scalars(stmt):
                db_device = device
            if db_device is None:
                db_device = Device(id=device_id)
            if device_name:
                db_device.name = device_name
            elif not db_device.name:
                db_device.name = "TYPE_%d" % device_id
            if room_id:
                db_device.room_id = room_id
            session.add_all([db_device])
            session.commit()
            session.refresh(db_device)
            return db_device

    def add_or_update_room(
        self,
        room_id: int = None,
        room_name: str = None,
        group_id: int = None
    ) -> None:
        """update or add a room

        Args:
            room_id (int, optional): Room id to be modified (if None a new Room is added), Default to None.
            room_name (str, optional): Roomname wich should be set or updated. Defaults to None.

        Returns:
            _type_: _description_
        """
        with Session(self._engine) as session:
            stmt = select(Room).where(Room.id == room_id)
            db_room = None
            for room in session.scalars(stmt):
                db_room = room
            if db_room is None:
                db_room = Room(id=room_id)
            if room_name:
                db_room.name = room_name
            elif not db_room.name:
                db_room.name = "NAME_%d" % room_id
            if group_id:
                db_room.group_id = group_id
            elif not db_room.name:
                db_room.name = 1
            session.add_all([db_room])
            session.commit()
            session.refresh(db_room)
            return db_room

    def get_room(self, room_id=None) -> Room:
        with Session(self._engine) as session:
            stmt = select(Room).where(Room.id == room_id)
            return session.scalars(stmt).one()

    def get_rooms(self) -> List[Room]:
        """Get all configured rooms

        Returns:
            List[Room]: List of Room objects. 
        """
        with Session(self._engine) as session:
            stmt = select(Room)
            return session.scalars(stmt).all()

    def add_or_update_room_group(
        self,
        room_group_id: int = None,
        room_group_name: str = None
    ) -> None:
        """update or add a room_group

        Args:
            room_group_id (int, optional): RoomGroup id to be modified (if None a new RoomGroup is added), Default to None.
            room_group_name (str, optional): RoomGroupname wich should be set or updated. Defaults to None.

        Returns:
            _type_: _description_
        """
        with Session(self._engine) as session:
            stmt = select(RoomGroup).where(RoomGroup.id == room_group_id)
            db_room_group = None
            for room_group in session.scalars(stmt):
                db_room_group = room_group
            if db_room_group is None:
                db_room_group = RoomGroup(id=room_group_id)
            if room_group_name:
                db_room_group.name = room_group_name
            elif not db_room_group.name:
                db_room_group.name = "NAME_%d" % room_group_id
            session.add_all([db_room_group])
            session.commit()
            session.refresh(db_room_group)
            return db_room_group

    def get_room_group(self, room_group_id=None) -> RoomGroup:
        with Session(self._engine) as session:
            stmt = select(RoomGroup).where(RoomGroup.id == room_group_id)
            return session.scalars(stmt).one()

    def get_room_groups(self) -> List[RoomGroup]:
        """Get all configured room_groups

        Returns:
            List[RoomGroup]: List of RoomGroup objects. 
        """
        with Session(self._engine) as session:
            stmt = select(RoomGroup)
            return session.scalars(stmt).all()
