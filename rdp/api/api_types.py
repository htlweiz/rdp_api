from pydantic import BaseModel

class ApiTypes(BaseModel):
    description: str = "This is the API"
    value_type_link: str = "/type"
    value_link: str = "/value"

class RoomGroup(BaseModel):
    id: int
    name: str

class Room(BaseModel):
    id: int
    name: str
    room_group_id: int

class Device(BaseModel):
    id: int
    name: str
    room_id: int

class ValueTypeNoID(BaseModel):
    type_name: str
    type_unit: str

class ValueType(ValueTypeNoID):
    id: int

class ValueNoID(BaseModel):
    value_type_id: int
    time: int
    value: float

class Value(ValueNoID):
    id: int
