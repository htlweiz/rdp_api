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
    device_id: int

class Value(ValueNoID):
    id: int

class DeviceNoID(BaseModel):
    device_name: str
    device_desc: str
    room_id: int

class Device(DeviceNoID):
    id: int

class RoomNoID(BaseModel):
    room_name: str
    location_id: int

class Room(RoomNoID):
    id: int

class LocationNoID(BaseModel):
    location: str

class Location(LocationNoID):
    id: int

class ApiDescription(BaseModel):
    description : str = "This is the Api"
    value_type_link : str = "/type"
    value_link : str = "/value"