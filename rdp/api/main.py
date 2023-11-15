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
def create_value(value:float, time:int, value_type_id:int):
    """Create a new value.

    Args:
        value (Value): The value to be created.

    Returns:
        Value: The created value.
    """
    global crud
    try:
        crud.add_value(value_time=time, value_type=value_type_id, value_value=value)
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

@app.get("/device/{id}/")
def read_device(id) -> ApiTypes.Device:
    """Implements the get of all devices

    Returns:
        List[ApiTypes.Device]: list of available devices. 
    """
    global crud
    return crud.get_device(id)

@app.put("/device/")
def put_device(device: ApiTypes.DeviceNoID) -> ApiTypes.Device:
    """PUT request to a specail device. This api call is used to change a device object.

    Args:
        id (int): primary key of the requested value type
        name (ApiTypes.ValueTypeNoID): json object representing the new state of the value type. 

    Raises:
        HTTPException: Thrown if a value type with the given id cannot be accessed 

    Returns:
        ApiTypes.ValueType: the requested value type after persisted in the database. 
    """
    global crud
    try:
        new_device = crud.add_or_update_device(device_name=device.name, room_id=device.room_id)
        return read_device(new_device.id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/room/")
def read_rooms() -> List[ApiTypes.Room]:
    """Implements the get of all rooms

    Returns:
        List[ApiTypes.Room]: list of available rooms. 
    """
    global crud
    return crud.get_rooms()

@app.get("/room/{id}")
def read_room(id) -> ApiTypes.Room:
    """Implements the get of all rooms

    Returns:
        List[ApiTypes.Room]: list of available rooms. 
    """
    global crud
    return crud.get_room(room_id=id)

@app.put("/room/")
def put_room(room: ApiTypes.RoomNoID) -> ApiTypes.Room:
    """PUT request to a specail room. This api call is used to change a room object.

    Args:
        id (int): primary key of the requested room
        name (ApiTypes.RoomNoID): json object representing the new state of the room. 

    Raises:
        HTTPException: Thrown if a room with the given id cannot be accessed 

    Returns:
        ApiTypes.Room: the requested room after persisted in the database. 
    """
    global crud
    try:
        new_room = crud.add_or_update_room(room_name=room.name, group_id=room.group_id)
        return read_room(new_room.id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/room_group/")
def read_room_groups() -> List[ApiTypes.RoomGroup]:
    """Implements the get of all room_groups

    Returns:
        List[ApiTypes.RoomGroup]: list of available room_groups. 
    """
    global crud
    return crud.get_room_groups()

@app.get("/room_group/{id}")
def read_room_group(id) -> ApiTypes.RoomGroup:
    """Implements the get of all room_groups

    Returns:
        List[ApiTypes.RoomGroup]: list of available room_groups. 
    """
    global crud
    return crud.get_room_group(room_group_id=id)

@app.put("/room_group/")
def put_room_group(room_group: ApiTypes.RoomGroupNoID) -> ApiTypes.RoomGroup:
    """PUT request to a specail room_group. This api call is used to change a room_group object.

    Args:
        id (int): primary key of the requested room_group
        name (ApiTypes.RoomGroupNoID): json object representing the new state of the room_group. 

    Raises:
        HTTPException: Thrown if a room_group with the given id cannot be accessed 

    Returns:
        ApiTypes.RoomGroup: the requested room_group after persisted in the database. 
    """
    global crud
    try:
        new_room_group = crud.add_or_update_room_group(room_group_name=room_group.name)
        return read_room_group(new_room_group.id)
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
    logger.debug("STARTUP: Sensore reader completed!")

@app.on_event("shutdown")
async def startup_event():
    """stop the character device reader
    """    
    global reader
    logger.debug("SHUTDOWN: Sensor reader!")
    reader.stop()
    logger.info("SHUTDOWN: Sensor reader completed!")
