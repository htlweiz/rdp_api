from typing import List

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ValueType(Base):
    __tablename__ = "value_type"
    value_type_id: Mapped[int] = mapped_column(primary_key=True)
    type_name: Mapped[str]
    type_unit: Mapped[str]

    values: Mapped[List["Value"]] = relationship(
        back_populates="value_type", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"ValueType(value_type_id={self.value_type_id!r}, value_type={self.type_name})"


class Value(Base):
    __tablename__ = "value"
    value_id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[int] = mapped_column()
    value: Mapped[float] = mapped_column()
    value_type_id: Mapped[int] = mapped_column(ForeignKey("value_type.value_type_id"))

    value_type: Mapped["ValueType"] = relationship(back_populates="values")

    __table_args__ = (
        UniqueConstraint("time", "value_type_id", name="value integrity"),
    )

    def __repr__(self) -> str:
        return_value = f"Value(value_id={self.value_id!r}, value_time={self.time!r} "
        return_value += f"value_type={self.value_type.type_name!r}, value={self.value})"
        return return_value
