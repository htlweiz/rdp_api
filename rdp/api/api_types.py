from pydantic import BaseModel

class ValueTypeNoID(BaseModel):
    type_name : str

class ValueType(ValueTypeNoID):
    id : int
    type_name : str

    