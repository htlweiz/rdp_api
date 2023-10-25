import logging
from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from .model import Base, Value, ValueType, Device, Room


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
        value_type_unit: str = None
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
            session.refresh(db_type)
            return db_type

    def add_value(self, value_time: int, value_type: int, value_value: float, device_id: int=None) -> None:
        """Add a measurement point to the database.

        Args:
            value_time (int): unix time stamp of the value.
            value_type (int): Valuetype id of the given value. 
            value_value (float): The measurement value as float.
        """        
        print("akfjöladjföajflöajldfkajölfja")
        with Session(self._engine) as session:
            stmt = select(ValueType).where(ValueType.id == value_type)
            db_type = self.add_or_update_value_type(value_type)
            db_device = self.add_or_update_device(device_id)
            db_value = Value(time=value_time, value=value_value, value_type=db_type, device=db_device)

            session.add_all([db_type, db_device, db_value])
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


    def get_device(self, id):
            
        with Session(self._engine) as session:
            stmt = select(Device).where(Device.id == id)
            return session.scalars(stmt).one()
    

    def add_or_update_device(
        self,
        device_id: int = None,
        device_name: str = None,
    ) -> None:

        logging.error("select statement worked!")
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
               db_device.name = "Device_%d" % device_id
            session.add_all([db_device])
            session.commit()
            session.refresh(db_device)
            return db_device


    def get_room(self, id):
            
        with Session(self._engine) as session:
            stmt = select(Room).where(Room.id == id)
            return session.scalars(stmt).one()
    

    def add_or_update_room(
        self,
        room_id: int = None,
        room_name: str = None,
    ) -> None:

        logging.error("select statement worked!")
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
               db_room.name = "Room_%d" % room_id
            session.add_all([db_room])
            session.commit()
            return db_room