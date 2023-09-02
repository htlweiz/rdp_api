from pydantic import BaseModel

class ValueTypeNoID(BaseModel):
    type_name : str
    type_unit : str

class ValueType(ValueTypeNoID):
    id : int
    