import logging
from typing import List

from sqlalchemy import select
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

    def add_value(self, value_time: int, value_type: int, value_value: float, device_id:int ) -> None:
        """Add a measurement point to the database.

        Args:
            value_time (int): unix time stamp of the value.
            value_type (int): Valuetype id of the given value. 
            value_value (float): The measurement value as float.
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
        self, value_type_id: int = None, start: int = None, 
        end: int = None, device_id: int = None
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

    """David Torbics 

    START"""

    def add_or_update_device(
        self, 
        device_id: int = None, 
        device_name: str = None, 
        room_id: int = None
    ) -> None:
        """_summary_

        Args:
            device_id (int, optional): _description_. Defaults to None.
            device_name (str, optional): _description_. Defaults to None.
        """
        print()
        with Session(self._engine) as session:
            stmt = select(Device).where(Device.id == device_id)
            db_type = None
            for type in session.scalars(stmt):
                db_type = type
            if db_type is None:
                db_type = Device(id=device_id)
            if device_name:
                db_type.name = device_name
            elif not db_type.device_name:
                db_type.device_name = "NONAME_%d" % device_id
            if room_id:
                db_type.room_id = room_id
            elif not db_type.room_id:
                db_type.room_id = "NOROOM_%d" % room_id
            session.add_all([db_type])
            session.commit()
            return db_type

    def get_device(self, device_id:int = None, type_id:int = None) -> Device:
        """_summary_

        Args:
            device_id (int, optional): _description_. Defaults to None.
            type_id (int, optional): _description_. Defaults to None.

        Returns:
            List[Device]: _description_
        """
        logging.error("getting device")
        with Session(self._engine) as session:
            if device_id is not None:
                stmt = select(Device).where(Device.id == device_id)
                logging.error(session.scalars(stmt).one())
            return session.scalars(stmt).one()

    def get_values_by_device_id(self, device_id:int = None) -> List[Value]:
        """_summary_

        Args:
            device_id (int, optional): _description_. Defaults to None.
            type_id (int, optional): _description_. Defaults to None.

        Returns:
            List[Value]: _description_
        """
        print()
        logging.warning(device_id)
        with Session(self._engine) as session:
            if device_id is not None:
                logging.error("searching...")
                stmt = select(Value).where(Value.device_id == device_id)
                logging.error(session.scalars(stmt).all())
            return session.scalars(stmt).all()

    def add_or_update_room(self, room_id, this_room_name, room_group_id) -> None:
        """_summary_

        Args:
            room_id (_type_): _description_
            room_name (_type_): _description_
            room_group (_type_): _description_

        Returns:
            _type_: _description_
        """
        with Session(self._engine) as session:
            stmt = select(Room).where(Room.id == room_id)
            db_type = None
            for type in session.scalars(stmt):
                db_type = type
            if db_type is None:
                db_type = Room(id=room_id)
            if this_room_name:
                db_type.room_name = this_room_name
            elif not db_type.room_name:
                db_type.room_name = "NONAME_%d" % room_id
            if room_group_id:
                db_type.room_group_id = room_group_id
            elif not db_type.room_group_id:
                db_type.room_group_id = "NONAME_%d" % room_id
            logging.error(db_type)
            session.add_all([db_type])
            session.commit()
            return db_type

    def get_rooms(self) -> List[Room]:
        """_summary_

        Returns:
            List[Room]: _description_
        """
        with Session(self._engine) as session:
            stmt = select(Room)
            stmt = stmt.order_by(Room.id)
            return session.scalars(stmt).all()

    def get_room_by_id(self, room_id) -> Room:
        """_summary_

        Args:
            room_id (_type_): _description_

        Returns:
            Room: _description_
        """
        with Session(self._engine) as session:
            if room_id is not None:
                logging.error("searching...")
                stmt = select(Room).where(Room.id == room_id)
                logging.error(session.scalars(stmt).all())
            return session.scalars(stmt).one()

    def put_room_group(self, group_id, room_group_name) -> None:
        """_summary_

        Args:
            room_group_name (_type_): _description_

        Returns:
            _type_: _description_
        """
        with Session(self._engine) as session:
            stmt = select(RoomGroup).where(RoomGroup.id == group_id)
            db_type = None
            for type in session.scalars(stmt):
                db_type = type
            if db_type is None:
                db_type = RoomGroup(id=group_id)
            if room_group_name:
                db_type.room_group_name = room_group_name
            elif not db_type.room_group_name:
                db_type.room_group_name = "NONAME_%d" % group_id
            logging.error(db_type)
            session.add_all([db_type])
            session.commit()
            return db_type

    def get_room_group_by_id(self, group_id) -> RoomGroup:
        """_summary_

        Args:
            group_id (_type_): _description_

        Returns:
            RoomGroup: _description_
        """
        with Session(self._engine) as session:
            if group_id is not None:
                logging.error("searching...")
                stmt = select(RoomGroup).where(RoomGroup.id == group_id)
                logging.error(session.scalars(stmt).all())
            return session.scalars(stmt).one()
