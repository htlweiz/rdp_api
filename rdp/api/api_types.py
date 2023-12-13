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
    name: str

class Device(DeviceNoID):
    id: int
    location_id: int

class LocationNoID(BaseModel):
    name: str
    address: str

class Location(LocationNoID):
    id: int

class ApiDescription(BaseModel):
    description : str = "This is the Api"
    value_type_link : str = "/type"
    value_link : str = "/value"
