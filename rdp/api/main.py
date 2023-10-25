from typing import Union, List

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse

from rdp.sensor import Reader
from rdp.crud import create_engine, Crud
from . import api_types as ApiTypes
import logging

logger = logging.getLogger("rdp.api")
app = FastAPI()

@app.get("/")
def read_root() -> ApiTypes.ApiDescription:
    """This url returns a simple description of the api

    Returns:
        ApiTypes.ApiDescription: the Api description in json format 
    """    
    return ApiTypes.ApiDescription()

@app.get("/type/")
def read_types() -> List[ApiTypes.ValueType]:
    """Implements the get of all value types

    Returns:
        List[ApiTypes.ValueType]: list of available valuetypes. 
    """    
    global crud
    return crud.get_value_types()

@app.get("/type/{id}/")
def read_type(id: int) -> ApiTypes.ValueType:
    """returns an explicit value type identified by id

    Args:
        id (int): primary key of the desired value type

    Raises:
        HTTPException: Thrown it a value type with the given id cannot be accessed

    Returns:
        ApiTypes.ValueType: the desired value type 
    """
    global crud
    try:
         return crud.get_value_type(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found") 
    return value_type 

@app.put("/type/{id}/")
def put_type(id, value_type: ApiTypes.ValueTypeNoID) -> ApiTypes.ValueType:
    """PUT request to a specail valuetype. This api call is used to change a value type object.

    Args:
        id (int): primary key of the requested value type
        value_type (ApiTypes.ValueTypeNoID): json object representing the new state of the value type. 

    Raises:
        HTTPException: Thrown if a value type with the given id cannot be accessed 

    Returns:
        ApiTypes.ValueType: the requested value type after persisted in the database. 
    """
    global crud
    try:
        crud.add_or_update_value_type(id, value_type_name=value_type.type_name, value_type_unit=value_type.type_unit)
        return read_type(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/value/")
def get_device(type_id:int=None, start:int=None, end:int=None) -> List[ApiTypes.Value]:
    """Get values from the database. The default is to return all available values. This result can be filtered.

    Args:
        type_id (int, optional): If set, only values of this type are returned. Defaults to None.
        start (int, optional): If set, only values at least as new are returned. Defaults to None.
        end (int, optional): If set, only values not newer than this are returned. Defaults to None.

    Raises:
        HTTPException: _description_

    Returns:
        List[ApiTypes.Value]: _description_
    """
    global crud
    try:
        values = crud.get_values(type_id, start, end)
        return values
    except crud.NoResultFound:
        raise HTTPException(status_code=404, deltail="Item not found")

@app.on_event("startup")
async def startup_event() -> None:
    """start the character device reader
    """    
    logger.info("STARTUP: Sensor reader!")
    global reader, crud
    engine = create_engine("sqlite:///rdb.test.db")
    crud = Crud(engine)
    reader = Reader(crud)
    reader.start()
    logger.debug("STARTUP: Sensore reader completed!")

@app.on_event("shutdown")
async def startup_event():
    """stop the character device reader
    """    
    global reader
    logger.debug("SHUTDOWN: Sensor reader!")
    reader.stop()
    logger.info("SHUTDOWN: Sensor reader completed!")

@app.get("/device/{id}")
def get_device(id:int=None) -> ApiTypes.DeviceNoID: 
    global crud
    try:
        device = crud.get_device(id)
        return device
    except crud.NoResultFound:
        raise HTTPException(status_code=404, deltail="Item not found")

@app.put("/device/{id}")
def put_device(id, device_name: ApiTypes.DeviceNoID) -> ApiTypes.Device:
    global crud
    logging.error("select statement worked!")
    try:
        crud.add_or_update_device(id, device_name.name)
        return get_device(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")
        

@app.put("/room/{id}")
def put_room(id, room_name: ApiTypes.RoomNoID) -> ApiTypes.Room:
    global crud
    try:
        crud.add_or_update_room(id, room_name.name)
        return get_room(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/room/{id}")
def get_room(id:int=None) -> ApiTypes.RoomNoID: 
    global crud
    try:
        room = crud.get_room(id)
        return room
    except crud.NoResultFound:
        raise HTTPException(status_code=404, deltail="Item not found")


@app.post("/import_csv/")
async def import_csv(file: UploadFile = File(...)):
    
    file_content = await file.read()
    parse_csv(file_content.decode('utf-8'), file.filename)


    logger.error("CSV File Content:")
    logger.error(file_content)


    return "CSV File added!"


def parse_csv(content, filename):
    rows = []
    value_types = []
    raw_rows = content.split("\n")
    for raw_row in raw_rows:
        if raw_row == raw_rows[0]:
            value_types = raw_row.split(',')
        else:
            one_line = raw_row.split(',')
            # for x in one_line:
            #     if x != one_line[0]:
            for x in range(len(one_line)):
                if x != 0:
                    crud.add_value(value_time=one_line[0],
                                   value_type=crud.add_or_update_value_type(value_type_name=value_types[x],value_type_unit="bogus_unit").id,
                                   value_value=one_line[x], device_id=crud.add_or_update_device(device_name=filename).id)
        # rows.append(one_line)

