from typing import Union

from fastapi import FastAPI

from rdp.sensor import Reader, LOGGER_TO_USE
from rdp.crud import create_engine, SensorCrud

import logging

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.on_event("startup")
async def startup_event():
    print("ON EVENT Startup!!!!")
    engine = create_engine("sqlite:///rdb.test.db")
    crud = SensorCrud(engine)
    global reader
    reader = Reader(crud)
    reader.start()
    print("Reader started")

@app.on_event("shutdown")
async def startup_event():
    print("ON EVENT Shutdown!!!!")
    global reader
    reader.stop()
    print("Reader stopped")