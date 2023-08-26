from typing import Union, List

from fastapi import FastAPI, HTTPException

from rdp.sensor import Reader, LOGGER_TO_USE
from rdp.crud import create_engine, SensorCrud
from . import api_types as ApiTypes
import logging

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/type/")
def read_types() -> List[ApiTypes.ValueType]:
    return crud.get_value_types()

@app.get("/type/{id}/")
def read_type(id) -> ApiTypes.ValueType:
    try:
         return crud.get_value_type(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found") 
    return value_type 

@app.put("/types/{id}/")
def put_type(id, value_type: ApiTypes.ValueTypeNoID) -> ApiTypes.ValueType:
    try:
        crud.change_value_name(id, value_type.type_name)
        return read_type(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/types/{id}/values/")
def get_values(id, start=None, end=None):
    try:
        values = crud.get_values(id, start, end)
        return values
    except crud.NoResultFound:
        raise HTTPException(status_code=404, deltail="Item not found")

@app.on_event("startup")
async def startup_event():
    global reader, crud
    print("ON EVENT Startup!!!!")
    engine = create_engine("sqlite:///rdb.test.db")
    crud = SensorCrud(engine)
    reader = Reader(crud)
    reader.start()
    print("Reader started")

@app.on_event("shutdown")
async def startup_event():
    global reader
    print("ON EVENT Shutdown!!!!")
    reader.stop()
    print("Reader stopped")