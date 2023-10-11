from pydantic import BaseModel

class ValueTypeNoID(BaseModel):
    type_name : str
    type_unit : str

class ValueType(ValueTypeNoID):
    id : int

class ValueNoID(BaseModel):
    value_type_id: int
    time: int
    value: float 

class Value(ValueNoID):
    id: int

class ApiDescription(BaseModel):
    description : str = "This is the Api"
    value_type_link : str = "/type"
    value_link : str = "/value"

class DeviceNoID(BaseModel):
    name: str = "name"
    
class Device(DeviceNoID):
    id: int

class RoomNoID(BaseModel):
    name: str = "name"
    room_id: int = 0

class Room(RoomNoID):
    id: int
