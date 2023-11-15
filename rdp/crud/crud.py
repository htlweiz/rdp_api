import logging
from typing import List
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from datetime import datetime
from .model import Base, Value, ValueType, Device, Room, RoomGroup

class Crud:
    def __init__(self, engine):
        self._engine = engine

        Base.metadata.create_all(self._engine)

    def add_or_update_value_type(
        self,
        value_type_id: int = None,
        value_type_name: str = "TYPE",
        value_type_unit: str = "UNIT",
    ) -> ValueType:
        with Session(self._engine) as session:
            db_type = session.query(ValueType).filter_by(id=value_type_id).one_or_none() if value_type_id is not None else None

            if db_type is None:
                db_type = ValueType()
            if value_type_name:
               db_type.type_name = value_type_name
            if value_type_unit:
                db_type.type_unit = value_type_unit

            session.add(db_type)
            session.commit()
            return db_type

    def add_value(self, value_time: int, value_type: int, value_value: float) -> None:
        try:
            with Session(self._engine) as session:
                db_type = session.query(ValueType).filter_by(id=value_type).one()

                value_time = datetime.fromtimestamp(value_time)
                db_value = Value(time=value_time, value=value_value, value_type=db_type)
                session.add(db_value)

                try:
                    session.commit()
                except IntegrityError:
                    logging.error("Integrity error")
                    raise
        except NoResultFound:
            logging.error("Value type not found.")

    def get_value_types(self) -> List[ValueType]:
        with Session(self._engine) as session:
            value_types = session.query(ValueType).all()
            return value_types

    def get_value_type(self, value_type_id: int) -> ValueType:
        with Session(self._engine) as session:
            return session.query(ValueType).filter_by(id=value_type_id).one()

    def get_values(
        self, value_type_id: int = None, start: int = None, end: int = None
    ) -> List[Value]:
        with Session(self._engine) as session:
            stmt = select(Value)
            if value_type_id is not None:
                stmt = stmt.join(Value.value_type).filter(ValueType.id == value_type_id)
            if start is not None:
                start = datetime.fromtimestamp(start)
                stmt = stmt.filter(Value.time >= start)
            if end is not None:
                end = datetime.fromtimestamp(end)
                stmt = stmt.filter(Value.time <= end)
            stmt = stmt.order_by(Value.time)

            return stmt.all()

    def add_or_update_device(self, name: str, room_id: int) -> Device:
        with Session(self._engine) as session:
            db_device = session.query(Device).filter_by(device_name=name).one_or_none()
            if db_device is None:
                db_device = Device(device_name=name, room_id=room_id)
            else:
                db_device.room_id = room_id
            session.add(db_device)
            session.commit()
            return db_device

    def get_device(self, device_id: int) -> Device:
        with Session(self._engine) as session:
            return session.query(Device).filter_by(id=device_id).one()

    def get_device_values(self, device_id: int, value_type_id: int) -> List[Value]:
        with Session(self._engine) as session:
            stmt = (
                select(Value)
                .join(Value.value_type)
                .join(Value.device)
                .filter(Device.id == device_id)
                .filter(ValueType.id == value_type_id)
            )
            stmt = stmt.order_by(Value.time)
            return stmt.all()

    def add_or_update_room(self, name: str, room_group_id: int) -> Room:
        with Session(self._engine) as session:
            db_room = session.query(Room).filter_by(room_name=name).one_or_none()
            if db_room is None:
                db_room = Room(room_name=name, room_group_id=room_group_id)
            else:
                db_room.room_group_id = room_group_id
            session.add(db_room)
            session.commit()
            return db_room

    def get_room(self, room_id: int) -> Room:
        with Session(self._engine) as session:
            return session.query(Room).filter_by(id=room_id).one()

    def get_room_by_group(self, group_id: int) -> Room:
        with Session(self._engine) as session:
            return session.query(Room).filter_by(room_group_id=group_id).one()

    def add_or_update_group(self, group_id: int = None) -> RoomGroup:
        with Session(self._engine) as session:
            if group_id is not None:
                db_group = session.query(RoomGroup).filter_by(id=group_id).one_or_none()
            else:
                db_group = None

            if db_group is None:
                db_group = RoomGroup()
            session.add(db_group)
            session.commit()
            return db_group