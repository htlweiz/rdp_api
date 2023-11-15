from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class ValueType(Base):
    """Defines the ValueType table."""
    __tablename__ = "value_type"
    id = Column(Integer, primary_key=True)
    type_name = Column(String)
    type_unit = Column(String)

    values = relationship("Value", back_populates="value_type", cascade="all, delete-orphan")

    def __repr__(self):
        return f"ValueType(id={self.id!r}, type_name={self.type_name!r}, type_unit={self.type_unit!r})"

class Value(Base):
    """Defines the Value table."""
    __tablename__ = "value"
    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    value = Column(Float)
    value_type_id = Column(Integer, ForeignKey("value_type.id"))

    value_type = relationship("ValueType", back_populates="values")

    __table_args__ = (
        UniqueConstraint("time", "value_type_id", name="value_integrity"),
    )

    def __repr__(self):
        return f"Value(id={self.id!r}, time={self.time!r}, type_name={self.value_type.type_name!r}, value={self.value!r})"

class Device(Base):
    """Defines the Device table."""
    __tablename__ = "device"
    id = Column(Integer, primary_key=True)
    device_name = Column(String)
    room_id = Column(Integer, ForeignKey("room.id"))

    def __repr__(self):
        return f"Device(id={self.id!r}, device_name={self.device_name!r}, room_id={self.room_id!r})"

class Room(Base):
    """Defines the Room table."""
    __tablename__ = "room"
    id = Column(Integer, primary_key=True)
    room_name = Column(String)
    room_group_id = Column(Integer, ForeignKey("room_group.id"))

    def __repr__(self):
        return f"Room(id={self.id!r}, room_name={self.room_name!r}, room_group_id={self.room_group_id!r})"

class RoomGroup(Base):
    """Defines the RoomGroup table."""
    __tablename__ = "room_group"
    id = Column(Integer, primary_key=True)
    room_group_name = Column(String)

    def __repr__(self):
        return f"RoomGroup(id={self.id!r}, room_group_name={self.room_group_name!r})"
