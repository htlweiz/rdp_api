from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, UniqueConstraint

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class Sensor(Base):
    __tablename__ = "sensor"
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    location: Mapped[str]

    def __repr__(self) -> str:
        return f"Sensor(id={self.id!r}, name={self.name})"


class ValueType(Base):
    __tablename__ = "value_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    type_name: Mapped[str]
    type_unit: Mapped[str]

    values: Mapped[List["Value"]] = relationship(back_populates="value_type", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"ValueType(id={self.id!r}, value_type={self.type_name})"


class Value(Base):
    __tablename__ = "value"
    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[int] = mapped_column()
    value: Mapped[float] = mapped_column()
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensor.id"))

    value_type_id: Mapped[int] = mapped_column(ForeignKey("value_type.id"))
    value_type: Mapped["ValueType"] = relationship(back_populates="values")

    def __repr__(self) -> str:
        return f"Value(id={self.id!r}, value_time={self.time!r} value_type={self.value_type.type_name!r}, value={self.value}, sensor_id={self.sensor_id})"
