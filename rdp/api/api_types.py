from pydantic import BaseModel

class DeviceNoID(BaseModel):
    name: str
    device: str
    postalCode: int
    city: str
    room_id: int

class Device(DeviceNoID):
    id: int

class ValueTypeNoID(BaseModel):
    type_name: str
    type_unit: str


class ValueType(ValueTypeNoID):
    id: int


class ValueNoID(BaseModel):
    value_type_id: int
    time: int
    value: float
    device_id: int


class Value(ValueNoID):
    id: int

class RoomNoID(BaseModel):
    name: str
    room_nr: int
    location_id: int
    

class Room(RoomNoID):
    id: int

class LocationNoId(BaseModel):
    name: str
    city: str

class Location(LocationNoId):
    id: int

class ApiDescription(BaseModel):
    description: str = "This is the Api"
    value_type_link: str = "/type"
    value_link: str = "/value"
    device_link: str = "/device"
    room_link: str = "/room"
    location_link: str = "/location"

