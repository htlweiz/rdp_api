from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Float

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import sessionmaker

class Base(DeclarativeBase):
    pass

class ValueType(Base):
    __tablename__ ="value_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    type_name: Mapped[Optional[str]]
    
    def __repr__(self) -> str:
        return f"ValueType(id={self.id!r}, value_type={self.type_name})"

class Value(Base):
    __tablename__ = "value"
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[float] = mapped_column()
    value_type: Mapped["ValueType"] = relationship(back_populates="values")

    def __repr__(self) -> str:
        return f"Value(id={self.id!r}, value_type={self.value_type.type_name!r}, value={self.value})" 
