from typing import List, Dict
from pydantic import BaseModel


class ValueTypeNoID(BaseModel):
    type_name: str
    type_unit: str


class ValueType(ValueTypeNoID):
    id: int


class ValueNoID(BaseModel):
    value_type_id: int
    device_id: int
    time: int
    value: float


class DeviceNoID(BaseModel):
    name: str
    device: str
    room_id: int | None = None


class Device(DeviceNoID):
    id: int


class Value(ValueNoID):
    id: int


class ApiDescription(BaseModel):
    description: str = "This is the Api"
    value_type_link: str = "/type"
    value_link: str = "/value"


class RoomNoID(BaseModel):
    name: str
    room_group_id: int | None = None


class Room(RoomNoID):
    id: int


class RoomGroupNoID(BaseModel):
    name: str
    room_group_id: int | None = None


class RoomGroup(RoomGroupNoID):
    id: int


class CsvHeaderMapping(BaseModel):
    mappings: List[Dict[str, str]]
    device_id: int
