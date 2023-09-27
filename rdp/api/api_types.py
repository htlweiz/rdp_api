from pydantic import BaseModel


class ValueTypeNoID(BaseModel):
    type_name: str
    type_unit: str


class ValueType(ValueTypeNoID):
    id: int


class ValueNoID(BaseModel):
    value_type_id: int
    time: int
    value: float


class DeviceNoID(BaseModel):
    name: str
    device: str


class Device(BaseModel):
    id: int
    name: str
    device: str


class Value(ValueNoID):
    id: int


class ApiDescription(BaseModel):
    description: str = "This is the Api"
    value_type_link: str = "/type"
    value_link: str = "/value"
