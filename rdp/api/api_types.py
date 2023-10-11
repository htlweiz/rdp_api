from pydantic import BaseModel

class ValueTypeNoID(BaseModel):
    type_name : str
    type_unit : str

class ValueType(ValueTypeNoID):
    id : int

class ValueNoID(BaseModel):
    value_type_id: int
    device_id: int
    time: int
    value: float 

class Value(ValueNoID):
    id: int

class DeviceNoID(BaseModel):
    name: str
    room_id: int

class Device(DeviceNoID):
    id: int

class RoomNoId(BaseModel):
    room_name: str
    room_group_id: int

class Room(RoomNoId):
    id: int

class RoomGroupNoId(BaseModel):
    room_group_name: str

class RoomGroup(RoomGroupNoId):
    id: int

class ApiDescription(BaseModel):
    description : str = "This is the Api"
    value_type_link : str = "/type"
    value_link : str = "/value"
    device_link : str = "/device"
    room_link : str = "/room"
    room_group_link : str = "/room_group"