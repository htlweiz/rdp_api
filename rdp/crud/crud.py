import logging
from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from .model import Base, Value, ValueType, Device, Location


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

    def add_value(self, value_time: int, value_type: int, value_value: float, value_device: int) -> None:
        """Add a measurement point to the database.

        Args:
            value_time (int): unix time stamp of the value.
            value_type (int): Valuetype id of the given value. 
            value_value (float): The measurement value as float.
        """        
        with Session(self._engine) as session:
            stmt = select(ValueType).where(ValueType.id == value_type)
            stmt = select(Device).where(Device.id == value_device)
            db_type = self.add_or_update_value_type(value_type)
            # db_device = self.add_device('test', 'testloc')
            db_value = Value(time=value_time, value=value_value, device_id=value_device, value_type=db_type)

            session.add_all([db_value, db_type])
            try:
                session.commit()
            except IntegrityError:
                logging.error("Integrity")
                raise

    def add_device(self, _name: str, _location_id: int, _type: str) -> int:
        """Add a device to the database.

        Args:
            name (str): A name for the device
            location_id (int): A location to the device
        """
        with Session(self._engine) as session:
            stmt = select(Device).where(Device.name == _name)
            result = session.execute(stmt)
            db_device = result.scalars().all()

            if db_device == []:
                db_device = Device(name=_name, location_id=_location_id, device_type=_type)

                session.add(db_device)
                try:
                    session.commit()
                    return db_device.id
                except IntegrityError:
                    logging.error("Integrity")

    def add_location(self, _name: str, _address: str) -> int:
        """Add a device to the database.

        Args:
            _name (str): A name for the location
            _address (int): An address for the location
        """
        with Session(self._engine) as session:
            stmt = select(Location).where(Location.name == _name)
            result = session.execute(stmt)
            db_location = result.scalars().first()

            if db_location is None:
                db_location = Location(name=_name, address=_address)
                session.add(db_location)

                try:
                    session.commit()
                    return db_location.id
                except IntegrityError:
                    logging.error("Integrity")
                    raise
            else:
                # If location already exists, you can decide how to handle it
                print("Location already exists with id:", db_location.id)
                return db_location.id

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
            self, value_type_id: int = None, start: int = None, end: int = None, device: int = None
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
            if device is not None:
                stmt = stmt.where(Value.device_id == device)
            stmt = stmt.order_by(Value.time)
            logging.error(start)
            logging.error(stmt)

            return session.scalars(stmt).all()

    def get_devices(self) -> List[Device]:
        with Session(self._engine) as session:
            stmt = select(Device)
            return session.scalars(stmt).all()

    def get_locations(self) -> List[Location]:
        with Session(self._engine) as session:
            stmt = select(Location)
            return session.scalars(stmt).all()

#    def order_values(self) -> List(ValueType):
#        """Sort the values.
#
#        Args:
#            self
#
#        Returns:
#            List[ValueType]: Sorted list.
#        """
#        with Session(self._engine) as session:
#            stmt = select(Value)
#            values = session.scalars(stmt).all()
#        values = sorted(values, key=lambda x: x.value)
#        return values

