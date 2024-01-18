import logging
from typing import List


from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from .model import Base, Value, ValueType, Device, Room, Location


class Crud:
    def __init__(self, engine):
        """
        Initializes Crud object with a SQLAlchemy engine.

        Args:
            engine: SQLAlchemy engine object.
        """
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
        """
        Update or add a value type.

        Args:
            value_type_id (int, optional): ValueType id to be modified (if None a new ValueType is added), Default to None.
            value_type_name (str, optional): Type name which should be set or updated. Defaults to None.
            value_type_unit (str, optional): Unit of measurement which should be set or updated. Defaults to None.

        Returns:
            ValueType: The modified or added ValueType object.
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
        self, value_time: int, value_type: int, device: int, value_value: float
    ) -> None:
        """
        Update or add a value type.

        Args:
            value_type_id (int, optional): ValueType id to be modified (if None a new ValueType is added), Default to None.
            value_type_name (str, optional): Type name which should be set or updated. Defaults to None.
            value_type_unit (str, optional): Unit of measurement which should be set or updated. Defaults to None.

        Returns:
            ValueType: The modified or added ValueType object.
        """
        with Session(self._engine) as session:
            stmt = select(ValueType).where(ValueType.id == value_type)
            db_type = self.add_or_update_value_type(value_type)
            db_value = Value(
                time=value_time, value=value_value, value_type=db_type, device_id=device
            )

            session.add_all([db_type, db_value])
            try:
                session.commit()
            except IntegrityError:
                logging.error("Integrity")
                raise

    def update_device(
        self, device_id: int = None, device_device: str = None, device_name: str = None, postalCode: int = None, city: str = None, room_id: int = None
    ) -> None:
        """
        Add or update a device in the database.

        Args:
            device_id (int, optional): The ID of the device.
            device_device (str, optional): The device information.
            device_name (str, optional): The device name.
            postalCode (int, optional): The postal code.
            city (str, optional): The city.
            room_id (int, optional): The ID of the room associated with the device.

        Raises:
            IntegrityError: If an integrity error occurs during the operation.
        """
        with Session(self._engine) as session:
            stmt = select(Device).where(Device.id == device_id)
            db_device = None
            for device in session.scalars(stmt):
                db_device = device
            if db_device is None:
                db_device = Device(device=device_device, name=device_name, postalCode=postalCode, city=city)
            if device_device:
                db_device.device = device_device
            if device_name:
                db_device.name = device_name
            if postalCode:
                db_device.postalCode = postalCode
            if city:
                db_device.city = city
            if room_id:
                db_device.room_id = room_id
            session.add(db_device)
            try:
                session.commit()
            except IntegrityError:
                logging.error("Integrity")
                raise

    def get_value_types(self) -> List[ValueType]:
        """
        Get a list of value types.

        Returns:
            List[ValueType]: A list of value types.
        """
        with Session(self._engine) as session:
            stmt = select(ValueType)
            return session.scalars(stmt).all()

    def get_value_type(self, value_type_id: int) -> ValueType:
        """
        Get a specific value type by ID.

        Args:
            value_type_id (int): The ID of the value type.

        Returns:
            ValueType: The value type corresponding to the ID.

        Raises:
            NoResultFound: If no result is found for the given ID.
        """
        with Session(self._engine) as session:
            stmt = select(ValueType).where(ValueType.id == value_type_id)
            return session.scalars(stmt).one()


    def get_values(
        self,
        value_type_id: int = None,
        start: int = None,
        end: int = None,
        device: str = None, #join device
    ) -> List[Value]:
        """
        Get values based on specified parameters.

        Args:
            value_type_id (int, optional): ID of the value type.
            start (int, optional): Start time.
            end (int, optional): End time.
            device (str, optional): Device name.

        Returns:
            List[Value]: A list of values based on the specified parameters.
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
                stmt = stmt.where(Value.device.name == device) #join device
            stmt = stmt.order_by(Value.time)
            logging.error(start)
            logging.error(stmt)

            return session.scalars(stmt).all()

    def get_values_order_by_time_and_id(self, value_type_id: int = None, start: int = None, end: int = None) -> List[Value]:
        """
        Get values ordered by value type ID and time.

        Args:
            value_type_id (int, optional): ID of the value type.
            start (int, optional): Start time.
            end (int, optional): End time.

        Returns:
            List[Value]: A list of values ordered by value type ID and time.
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
        Get values ordered by value type ID and value.

        Args:
            value_type_id (int, optional): ID of the value type.
            start (int, optional): Start time.
            end (int, optional): End time.

        Returns:
            List[Value]: A list of values ordered by value type ID and value.
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

    def get_devices(self) -> List[Device]:
        """
        Fetches all devices.

        Returns:
            List[Device]: A list of all devices.
        """
        with Session(self._engine) as session:
            stmt = select(Device)
            return session.scalars(stmt).all()

    def get_device(self, id: int):
        """
        Fetches a specific device by ID.

        Args:
            id (int): ID of the device.

        Returns:
            Device: The device object corresponding to the given ID.
        """
        with Session(self._engine) as session:
            stmt = select(Device).where(Device.id == id)
            return session.scalars(stmt).one()

    def update_room(self, room_id, room_name, room_nr, location_id) -> Room:
        """
        Adds or updates a room entry.

        Args:
            room_id: ID of the room.
            room_name: Name of the room.
            room_nr: Room number.
            location_id: ID of the location.

        Returns:
            Room: The updated room object.
        """
        new_id = None
        with Session(self._engine) as session:
            stmt = select(Room).where(Room.id == room_id)
            db_room = None
            for room in session.scalars(stmt):
                db_room = room
            if db_room is None:
                db_room = Room()
            if room_name:
                db_room.name = room_name
            if room_nr:
                db_room.room_nr = room_nr
            if location_id:
                db_room.location_id = location_id
            session.add(db_room)
            session.commit()
            session.refresh(db_room)
            new_id = db_room.id
        return self.get_room(new_id)

    def get_room(self, id: int) -> Room:
        """
        Fetches a specific room by ID.

        Args:
            id (int): ID of the room.

        Returns:
            Room: The room object corresponding to the given ID.
        """
        with Session(self._engine) as session:
            stmt = select(Room).where(Room.id == id)
            return session.scalars(stmt).one()

    def get_rooms(self) -> List[Room]:
        """
        Fetches all rooms.

        Returns:
            List[Room]: A list of all rooms.
        """
        with Session(self._engine) as session:
            stmt = select(Room)
            return session.scalars(stmt).all()

    def get_location(self, id: int) -> Room:
        """
        Fetches a specific location by ID.

        Args:
            id (int): ID of the location.

        Returns:
            Location: The location object corresponding to the given ID.
        """
        with Session(self._engine) as session:
            stmt = select(Location).where(Location.id == id)
            return session.scalars(stmt).one()

    def get_locations(self) -> List[Location]:
        """
        Fetches all locations.

        Returns:
            List[Location]: A list of all locations.
        """
        with Session(self._engine) as session:
            stmt = select(Location)
            return session.scalars(stmt).all()

    def get_value_by_device_id(self, device_id: int) -> List[Value]:
        """
        Fetches values based on a specific device ID.

        Args:
            device_id (int): ID of the device.

        Returns:
            List[Value]: A list of values associated with the given device ID.
        """
        with Session(self._engine) as session:
            stmt = select(Value).where(Value.device_id == device_id)
            return session.scalars(stmt).all()


    def update_location(self, location_id, location_name, city) -> Location:
        """
        Adds or updates a location entry.

        Args:
            location_id: ID of the location.
            location_name: Name of the location.
            city: City of the location.

        Returns:
            Location: The updated location object.
        """
        new_id = None
        with Session(self._engine) as session:
            stmt = select(Location).where(Location.id == location_id)
            db_location = None
            for location in session.scalars(stmt):
                db_location = location
            if db_location is None:
                db_location = Location()
            if location_name:
                db_location.name = location_name
            if city:
                db_location.city = city
            session.add(db_location)
            session.commit()
            session.refresh(db_location)
            new_id = db_location.id
        return self.get_location(new_id)

    def add_room(self, room_name: str, room_nr: int, location_id: int) -> Room:
        """
        Adds or updates a location entry.

        Args:
            location_id: ID of the location.
            location_name: Name of the location.
            city: City of the location.

        Returns:
            Location: The updated location object.
        """
        with Session(self._engine) as session:
            new_room = Room(name=room_name, room_nr=room_nr, location_id=location_id)
            session.add(new_room)
            session.commit()
            session.refresh(new_room)
            return new_room


    def add_location(self, location_name: str, city: str) -> Location:
        """
        Adds a new location entry.

        Args:
            location_name (str): Name of the location.
            city (str): City of the location.

        Returns:
            Location: The newly added location object.
        """
        with Session(self._engine) as session:
            new_location = Location(name=location_name, city=city)
            session.add(new_location)
            session.commit()
            session.refresh(new_location)
            return new_location

    def add_device(self, device_device: str, device_name: str, postalCode: int, city: str, room_id: int = None) -> Device:
        """
        Adds a new device entry.

        Args:
            device_device (str): Device type.
            device_name (str): Name of the device.
            postalCode (int): Postal code.
            city (str): City of the device.
            room_id (int, optional): ID of the associated room.

        Returns:
            Device: The newly added device object.
        """
        with Session(self._engine) as session:
            new_device = Device(device=device_device, name=device_name, postalCode=postalCode, city=city, room_id=room_id)
            session.add(new_device)
            session.commit()
            session.refresh(new_device)
            return new_device

   
    def add_new_value(self, value_time: int, value_type_id: int, device_id: int, value_value: float) -> None:
            with Session(self._engine) as session:
                try:
                    new_value = Value(
                        time=value_time,
                        value_type_id=value_type_id,
                        device_id=device_id,
                        value=value_value
                    )
                    session.add(new_value)
                    session.commit()
                except IntegrityError:
                    session.rollback()
                    raise
