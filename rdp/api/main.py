from typing import Union, List

from fastapi import FastAPI, HTTPException

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

@app.get("/device/")
def get_devices() -> List[ApiTypes.Device]:
    """GET request to retrieve a list of devices.

    Returns:
        List[ApiTypes.Device]: List of device objects.
    """
    global crud
    try:
        devices = crud.get_devices()
        return devices
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/location/")
def get_locations() -> List[ApiTypes.Location]:
    """GET request to retrieve a list of locations.

    Returns:
        List[ApiTypes.Location]: List of location objects.
    """
    global crud
    try:
        locations = crud.get_locations()
        return locations
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.post("/add_device/")
def add_device(name: str, location_id: int):
    """POST request to add a new device.

    Args:
        name (str): Name of the new device.
        location_id (int): ID of the location where the device is located.

    Returns:
        int: ID of the newly added device.
    """
    global crud
    try:
        device_id = crud.add_device(name, location_id)
        return device_id
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Could not add device")

@app.post("/add_location/")
def add_location(name: str, address: str):
    """POST request to add a new location.

    Args:
        name (str): Name of the new location.
        address (str): Address of the new location.

    Returns:
        int: ID of the newly added location.
    """
    global crud
    try:
        location_id = crud.add_location(name, address)
        return location_id
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Could not add Location")

@app.post("/add_type/")
def add_type(type_id: int, type_name: str, type_unit: str):
    """POST request to add or update a value type.

    Args:
        type_id (int): ID of the value type.
        type_name (str): Name of the value type.
        type_unit (str): Unit of the value type.

    Raises:
        HTTPException: Thrown if the value type cannot be added or updated.
    """
    global crud
    try:
        location = crud.add_or_update_value_type(type_id, type_name, type_unit)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Could not add Type")

@app.post("/add_value/")
def add_value(value_time: int, value_type: int, value_value: float, value_device: int):
    """POST request to add a new value.

    Args:
        value_time (int): Timestamp of the value.
        value_type (int): ID of the value type.
        value_value (float): Value of the new value.
        value_device (int): ID of the device associated with the value.

    Raises:
        HTTPException: Thrown if the value cannot be added.
    """
    global crud
    try:
        location = crud.add_value(value_time, value_type, value_value, value_device)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Could not add Value")

@app.get("/value/")
def get_values(type_id:int=None, start:int=None, end:int=None, device:int=None) -> List[ApiTypes.Value]:
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
        values = crud.get_values(type_id, start, end, device)
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
async def shutdown_event():
    """stop the character device reader
    """
    global reader
    logger.debug("SHUTDOWN: Sensor reader!")
    reader.stop()
    logger.info("SHUTDOWN: Sensor reader completed!")
