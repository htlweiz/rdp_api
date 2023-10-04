from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, Column, Integer, String, ForeignKey, Float, UniqueConstraint
from sqlalchemy import String, Float, DateTime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import sessionmaker


class Base(DeclarativeBase):
    pass


class ValueType(Base):
    __tablename__ = "value_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    type_name: Mapped[str]
    type_unit: Mapped[str]

    values: Mapped[List["Value"]] = relationship(
        back_populates="value_type", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"ValueType(id={self.id!r}, value_type={self.type_name})"


class Value(Base):
    __tablename__ = "value"
    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[int] = mapped_column()
    value: Mapped[float] = mapped_column()
    value_type_id: Mapped[int] = mapped_column(ForeignKey("value_type.id"))

    value_type: Mapped["ValueType"] = relationship(back_populates="values")

    __table_args__ = (
        UniqueConstraint("time", "value_type_id", name="value integrity"),
    )

    def __repr__(self) -> str:
        return f"Value(id={self.id!r}, value_time={self.time!r} value_type={self.value_type.type_name!r}, value={self.value})"
"""
class Device(Base):
    __tablename__ = "value"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_colum()
    
    __table__args__ = (
        UniqueConstraint("name")
    )

    def __repr__(self) -> str:
        return f""
"""


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    device = Column(String(255))


    def __repr__(self):
        return f"Device(id={self.id!r}, name={self.name!r},device={self.device!r})"
