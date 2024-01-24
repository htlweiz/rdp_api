from typing import Union, List

from fastapi import FastAPI, HTTPException

from rdp.sensor import Reader
from rdp.crud import create_engine, Crud
from . import api_types as ApiTypes
import logging

logger = logging.getLogger("rdp.api")
app = FastAPI()

@app.get("/d")
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
        HTTPException: Thrown if a value type with the given id cannot be accessed

    Returns:
        ApiTypes.ValueType: the desired value type 
    """
    global crud
    try:
         return crud.get_value_type(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found") 
    return value_type 

@app.get("/room/{id}/")
def get_room(id: int) -> ApiTypes.Room:
    """returns an explicit room identified by id

    Args:
        id (int): primary key of the desired value type

    Raises:
        HTTPException: Thrown if a value type with the given id cannot be accessed

    Returns:
        ApiTypes.Room: the desired room 
    """
    global crud
    try:
         return crud.get_room(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/room/")
def get_rooms() -> List[ApiTypes.Room]:
    """Implements the get of all rooms

    Returns:
        List[ApiTypes.Device]: list of available rooms. 
    """ 
    global crud
    return crud.get_rooms()

@app.get("/device/{id}/")
def get_device(id: int) -> ApiTypes.Device:
    """returns an explicit device identified by id

    Args:
        id (int): primary key of the desired value type

    Raises:
        HTTPException: Thrown if a value type with the given id cannot be accessed

    Returns:
        ApiTypes.Device: the desired device 
    """
    global crud
    try:
         return crud.get_device(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/device/")
def read_devices() -> List[ApiTypes.Device]:
    """Implements the get of all devices

    Returns:
        List[ApiTypes.Device]: list of available devices. 
    """ 
    global crud
    return crud.get_devices()

@app.put("/type/{id}/")
def put_type(id, value_type: ApiTypes.ValueTypeNoID) -> ApiTypes.ValueType:
    """PUT request to a special valuetype. This api call is used to change a value type object.

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

@app.put("/device/{id}/")
def put_device(id, device: ApiTypes.DeviceNoID) -> ApiTypes.Device:
    """PUT request to add a device. This api call is used to add a device with a name.

    Args:
        id (int): primary key of the requested device
        device_name (string):  

    Returns:
        ApiTypes.Device: _description_
    """
    global crud
    try:
        crud.add_or_update_device(id, device_name=device.device_name, device_desc=device.device_desc, room_id=1)
        return get_device(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.put("/room/{id}/")
def put_room(id, room: ApiTypes.RoomNoID) -> ApiTypes.Room:
    """PUT request to add a device. This api call is used to add a device with a name.

    Args:
        id (int): primary key of the requested device
        device_name (): 

    Returns:
        ApiTypes.Value: desired room values
    """
    global crud
    try:
        crud.add_or_update_room(id, room_name=room.room_name, location_id=1)
        return get_room(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.post("/room/{id}/")
def put_room(room: ApiTypes.RoomNoID) -> ApiTypes.Room:
    """POST request to add a room. This api call is used to add a room by autoincrementing the id.

    Args:
        id (int): primary key of the requested device
        room_name (string): name of the string 

    Returns:
        ApiTypes.Value: desired room values
    """
    global crud
    try:
        id = crud.add_or_update_room(room_name=room.room_name, location_id=1)
        return get_room(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/location/")
def get_locations() -> List[ApiTypes.Location]:
    """Implements the get of all locations

    Returns:
        List[ApiTypes.Device]: list of available locations. 
    """ 
    global crud
    return crud.get_locations()

@app.get("/value/{device_id}")
def get_values_by_device_id(device_id: int) -> List[ApiTypes.Value]:
    """Implements the get of all values by device_id

    Returns:
        List[ApiTypes.Device]: list of available locations. 
    """ 
    global crud
    return crud.get_value_by_device_id(device_id)

@app.get("/location/{id}/")
def get_location(id: int) -> ApiTypes.Location:
    """returns an explicit location identified by id

    Args:
        id (int): primary key of the desired location

    Raises:
        HTTPException: Thrown if a location with the given id cannot be accessed

    Returns:
        ApiTypes.Location: the desired location 
    """
    global crud
    try:
         return crud.get_location(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.put("/location/{id}/")
def put_locatation(id, location: ApiTypes.LocationNoID) -> ApiTypes.Location:
    """PUT request to add a location. This api call is used to add a location.

    Args:
        id (int): primary key of the requested location
        location (string): name of the location 

    Returns:
        ApiTypes.Location: the desired location
    """
    global crud
    try:
        crud.add_or_update_location(id, location=location.location)
        return get_location(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/value/")
def get_values(type_id:int=None, start:int=None, end:int=None) -> List[ApiTypes.Value]:
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

@app.post("/value/")
def put_values(value_time:int, value_type:int, value_value:float, device_id:int) -> List[ApiTypes.Value]:
    """Post values from the csv import.

    Args:
        type_id (int, optional): If set, only values of this type are returned. Defaults to None.

    Raises:
        HTTPException: _description_

    Returns:
        List[ApiTypes.Value]: _description_
    """
    global crud
    try:
        id = crud.add_value(value_time=value_time, value_type=value_type, value_value=value_value, device_id=device_id)
        return get_values(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

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
    logger.debug("STARTUP: Sensor reader completed!")

@app.on_event("shutdown")
async def shutdown_event():
    """stop the character device reader
    """    
    global reader
    logger.debug("SHUTDOWN: Sensor reader!")
    reader.stop()
    logger.info("SHUTDOWN: Sensor reader completed!")