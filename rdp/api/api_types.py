from pydantic import BaseModel


class ValueTypeNoID(BaseModel):
    type_name: str
    type_unit: str


class ValueType(ValueTypeNoID):
    value_type_id: int


class ValueNoID(BaseModel):
    value_type_id: int
    time: int
    value: float
    comment: str


class Value(ValueNoID):
    value_id: int


class ApiDescription(BaseModel):
    description: str = "This is the Api"
    value_type_link: str = "/type"
    value_link: str = "/value"
