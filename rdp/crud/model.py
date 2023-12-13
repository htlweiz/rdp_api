from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import String, Float, DateTime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import sessionmaker


class Base(DeclarativeBase):
    pass


class ValueType(Base):
    __tablename__ = "value_type"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type_name: Mapped[str]
    type_unit: Mapped[str]

    values = relationship("Value", back_populates="value_type", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"ValueType(id={self.id!r}, value_type={self.type_name})"

class Value(Base):
    __tablename__ = "value"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time: Mapped[int] = mapped_column()
    value: Mapped[float] = mapped_column()
    value_type_id: Mapped[int] = mapped_column(ForeignKey("value_type.id"))
    device_id: Mapped[int] = mapped_column(ForeignKey("device.id"))

    value_type = relationship("ValueType", back_populates="values")
    device: Mapped["Device"] = relationship(back_populates="values")
 
    __table_args__ = (UniqueConstraint("time", "value_type_id", "device_id", name="value_integrity"),)

    def __repr__(self) -> str:
        return f"Value(id={self.id!r}, value_time={self.time!r}, value_type={self.value_type.type_name!r}, value={self.value})"

class Device(Base):
    __tablename__ = "device"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    device_name: Mapped[str] = mapped_column()
    device_desc: Mapped[str] = mapped_column()
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"))

    values: Mapped[List["Value"]] = relationship(
        "Value", back_populates="device", cascade="all, delete-orphan"
    )
    room = relationship("Room", back_populates="rooms")

    def __repr__(self) -> str:
        return f"Device(id={self.id!r}, device_name={self.device_name!r}, device_desc={self.device_desc!r})"

class Room(Base):
    __tablename__ = "room"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    room_name: Mapped[str] = mapped_column()
    location_id: Mapped[int] = mapped_column(ForeignKey("location.id"))

    rooms: Mapped[List["Device"]] = relationship(
            "Device", back_populates="room", cascade="all, delete-orphan"
        )

    location = relationship("Location", back_populates="locations")

    def __repr__(self) -> str:
        return f"Room(id={self.id!r}, room_name={self.room_name!r}"

class Location(Base):
    __tablename__ = "location"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    location: Mapped[str] = mapped_column()

    locations: Mapped[List["Room"]] = relationship(
            "Room", back_populates="location", cascade="all, delete-orphan"
        )
    def __repr__(self) -> str:
        return f"Location(id={self.id!r}, location={self.room_name!r}"