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
    ApiTypes.ApiDescription.__name__ = "Hello"
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
        crud.add_or_update_value_type(id, value_time=value_type.time, type_id=value_type.value_type_id, value_value=value_type.value, device_id=value_type.device_id)
        return read_type(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.post("/value/")
def add_value(value: ApiTypes.ValueNoID): # -> ApiTypes.Value:
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
        crud.add_value(value_time=value.time, value_type_id=value.value_type_id, value_value=value.value, device_id=value.device_id)
        return 0 # crud.get_values(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Value could not be uploaded")

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


@app.put("/device/{id}/")
def put_device(id, device_name: ApiTypes.DeviceNoID) -> ApiTypes.Device:
    """PUT request to add a device. This api call is used to add a device with a name.

    Args:
        id (int): primary key of the requested device
        device_name (): 

    Returns:
        ApiTypes.Value: _description_
    """
    global crud
    try:
        crud.add_or_update_device(id, device_name=device_name.name, room_id=device_name.room_id)
        return get_device(id)
        # return 42
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/device/{id}")
def get_device(id:int=None) -> ApiTypes.Device:
    """_summary_

    Args:
        id (int, optional): _description_. Defaults to None.

    Returns:
        List[ApiTypes.Devices]: _description_
    """
    global crud
    try:
        device = crud.get_device(id)
        return device
    except Exception as e:
        return e

"""@app.put("/device/{id}/{type_id}/")
def put_values_by_device_and_type(device_id:int=None, type_id:int=None) -> List[ApiTypes.Value]:
    global crud
    try:
        values = crud.
"""        

@app.get("/value/{device_id}/")
def get_values_by_device_id(device_id:int=None) -> List[ApiTypes.Value]:
    global crud
    try:
        logging.error("searching...")
        values = crud.get_values_by_device_id(device_id)
        return values
    except:
        logging.error("failed...")
        return 0


@app.put("/room/{id}")
def put_room(id, room: ApiTypes.RoomNoId) -> ApiTypes.Room:
    """_summary_

    Raises:
        HTTPException: _description_

    Returns:
        ApiTypes.Room: _description_
    """
    global crud
    try:
        crud.add_or_update_room(id, this_room_name=room.room_name, room_group_id=room.room_group_id)
        return get_room_by_id(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/room/")
def get_rooms() -> List[ApiTypes.Room]:
    """_summary_

    Args:
        id (int): _description_

    Returns:
        List[ApiTypes.Room]: _description_
    """
    global crud
    try:
        rooms = crud.get_rooms()
        return rooms
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

@app.get("/room/{id}")
def get_room_by_id(id:int=None) -> ApiTypes.Room:
    """_summary_

    Args:
        id (int): _description_

    Returns:
        List[ApiTypes.Room]: _description_
    """
    global crud
    try:
        room = crud.get_room_by_id(id)
        return room
    except Exception as e:
        raise e

@app.put("/roomgroup/{id}")
def put_room_group(id, group: ApiTypes.RoomGroupNoId) -> ApiTypes.RoomGroup:
    """_summary_

    Args:
        id (_type_): _description_
        group (ApiTypes.RoomGroup): _description_

    Raises:
        HTTPException: _description_

    Returns:
        ApiTypes.RoomGroup: _description_
    """
    global crud
    try:
        crud.put_room_group(id, room_group_name=group.room_group_name)
        return get_room_group_by_id(id)
    except Exception as e:
        raise e

@app.get("/roomgroup/{id}")
def get_room_group_by_id(id:int=None) -> ApiTypes.RoomGroup:
    """_summary_

    Args:
        id (int, optional): _description_. Defaults to None.

    Raises:
        HTTPException: _description_

    Returns:
        ApiTypes.RoomGroup: _description_
    """
    global crud
    try:
        room = crud.get_room_group_by_id(id)
        return room
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

@app.on_event("startup")
async def startup_event() -> None:
    """start the character device reader"""    
    logger.info("STARTUP: Sensor reader!")
    global reader, crud
    engine = create_engine("sqlite:///rdb.test.db")
    crud = Crud(engine)
    reader = Reader(crud)
    reader.start()
    logger.debug("STARTUP: Sensor reader completed!")

@app.on_event("shutdown")
async def shutdown_event():
    global reader
    logger.debug("SHUTDOWN: Sensor reader!")
    reader.stop()
    logger.info("SHUTDOWN: Sensor reader completed!")
