from typing import List, Union
from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from rdp.crud import create_engine, Crud
from .api_types import ValueType, ValueTypeNoID, Value, ValueNoID, Device, Room, RoomGroup, ApiTypes
import logging

logger = logging.getLogger("rdp.api")
app = FastAPI()

engine = create_engine("sqlite:///rdb.test.db")
crud = Crud(engine)

def create_crud(engine: str = "sqlite:///rdb.test.db") -> Crud:
    return Crud(create_engine(engine))

@app.get("/")
def read_root():
    """This url returns a simple description of the API"""
    return {"message": "Welcome to the API!"}

@app.get("/type/")
def read_types() -> List[ValueType]:
    """Implements the GET request for all value types

    Returns:
        List[ValueType]: List of available value types
    """
    return crud.get_value_types()

@app.get("/type/{id}/")
def read_type(id: int) -> ValueType:
    """Returns an explicit value type identified by id

    Args:
        id (int): Primary key of the desired value type

    Raises:
        HTTPException: Thrown if a value type with the given id cannot be accessed

    Returns:
        ValueType: The desired value type
    """
    try:
        return crud.get_value_type(id)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@app.put("/type/{id}/")
def put_type(id: int, value_type: ValueTypeNoID) -> ValueType:
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
        db_value_type = crud.get_value_type(id)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    db_value_type.type_name = value_type.type_name
    db_value_type.type_unit = value_type.type_unit

    return crud.add_or_update_value_type(
        id=id, value_type_name=db_value_type.type_name, value_type_unit=db_value_type.type_unit
    )

@app.get("/value/")
def get_values(type_id: int = None, start: int = None, end: int = None) -> List[Value]:
    """Get values from the database. The default is to return all available values. This result can be filtered.

    Args:
        type_id (int, optional): If set, only values of this type are returned. Defaults to None.
        start (int, optional): If set, only values at least as new are returned. Defaults to None.
        end (int, optional): If set, only values not newer than this are returned. Defaults to None.

    Raises:
        HTTPException: Thrown if values are not found

    Returns:
        List[Value]: List of values
    """
    try:
        values = crud.get_values(type_id, start, end)
        return values
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.put("/device/{name}/")
def put_device(name: str, crud_instance: Crud = Depends(create_crud)) -> Device:
    """PUT request to create or update a device by name

    Args:
        name (str): The name of the device

    Returns:
        ApiTypes.Device: The created or updated device object
    """
    try:
        device = crud.add_or_update_device(name=name)
        return device
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Device already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/device/{id}/")
def get_device(id: int) -> Device:
    """GET request to retrieve information about a device by id

    Args:
        id (int): The unique identifier of the device

    Returns:
        ApiTypes.Device: Information about the device
    """
    try:
        device = crud.get_device(id)
        return device
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Device not found")

@app.get("/device/{id}/{type_id}/")
def get_device_values(id: int, type_id: int) -> List[Value]:
    """GET request to retrieve values for a specific device and value type

    Args:
        id (int): The unique identifier of the device
        type_id (int): The unique identifier of the value type

    Returns:
        List[Value]: List of values for the specified device and value type
    """
    try:
        values = crud.get_device_values(id, type_id)
        return values
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Values not found")

@app.put("/value/{device_id}/")
def put_value(device_id: int, value: ValueNoID) -> Value:
    """PUT request to add a new value for a specific device

    Args:
        device_id (int): The unique identifier of the device
        value (ApiTypes.Value): The value object to be added

    Returns:
        ApiTypes.Value: The added value object
    """
    try:
        added_value = crud.add_value(value.time, value.type_id, value.value)
        return added_value
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error")
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device or value type not found")

@app.get("/room/")
def get_room(id: int) -> Union[ApiTypes.Room, List[Room]]:
    """Get rooms from the database. The default is to return all available rooms

    Raises:
        HTTPException: Thrown if rooms are not found

    Returns:
        List[Room]: List of rooms
    """
    try:
        room = crud.get_room()
        return room
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/room/{id}/")
def get_room(id: int) -> Union[ApiTypes.Room, List[Room]]:
    """GET request to retrieve information about a room by id

    Args:
        id (int): The unique identifier of the room

    Returns:
        List[Room]: Information about the room
    """
    try:
        room = crud.get_room(id)
        return room
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Room not found")

@app.on_event("startup")
async def startup_event(crud: Crud = Depends(create_crud)):
    """Start the character device reader
    """
    global reader
    logger.info("STARTUP: Sensor reader!")
    reader = Reader(crud)
    reader.start()
    logger.debug("STARTUP: Sensor reader completed!")

@app.on_event("shutdown")
async def shutdown_event(reader: Reader = Depends(Reader)):
    """Stop the character device reader
    """
    logger.debug("SHUTDOWN: Sensor reader!")
    reader.stop()
    logger.info("SHUTDOWN: Sensor reader completed!")
