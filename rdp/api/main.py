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
        crud.add_or_update_value_type(
            id,
            value_type_name=value_type.type_name,
            value_type_unit=value_type.type_unit,
        )
        return read_type(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/value/")
def get_values(
    type_id: int = None, start: int = None, end: int = None, device: str = None
) -> List[ApiTypes.Value]:
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
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/value/")
def get_values_order_by_time_and_id(type_id: int = None, start: int = None, end: int = None) -> List[ApiTypes.Value]:
    """
    Retrieve values based on specified type ID, start, and end times, ordered by time and ID.

    Args:
        type_id (int, optional): The type ID for filtering values. Defaults to None.
        start (int, optional): The starting timestamp for filtering values. Defaults to None.
        end (int, optional): The ending timestamp for filtering values. Defaults to None.

    Returns:
        List[ApiTypes.Value]: A list of Value objects ordered by time and ID.

    Raises:
        HTTPException: If no results are found, raises a 404 status code with an error message.
    """
    global crud
    try:
        values = crud.get_values_order_by_time_and_id(type_id, start, end)
        return values
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")


## Order Values by ID & Value ##

#@app.get("/value/")
#def get_values_order_by_id_and_value(type_id:int=None, start:int=None, end:int=None) -> List[ApiTypes.Value]:
    """    Retrieve values based on specified type ID, start, and end times, ordered by value and ID.

    Args:
        type_id (int, optional): If set, only values of this type are returned. Defaults to None.
        start (int, optional): If set, only values at least as new are returned. Defaults to None.
        end (int, optional): If set, only values not newer than this are returned. Defaults to None.

    Raises:
        HTTPException: _description_

    Returns:
        List[ApiTypes.Value]: _description_
    """
#    global crud
#    try:
#        values = crud.get_values_order_by_id_and_value(type_id, start, end)
#        return values
#    except crud.NoResultFound:
#       raise HTTPException(status_code=404, deltail="Item not found")

@app.put("/device/{id}/")
def put_device(id, device: ApiTypes.DeviceNoID) -> ApiTypes.Device:
    """
    Updates or adds a device by its ID.

    Args:
        id (int): The ID of the device.
        device (ApiTypes.DeviceNoID): The device information.

    Returns:
        ApiTypes.Device: The updated device information.

    Raises:
        HTTPException: 
            - If the item is not found (status_code=404).
            - If there's an integrity error (status_code=400).
    """
    global crud
    try:
        crud.add_or_update_device(
            id, device_device=device.name, device_name=device.name
        )
        return get_device(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")
    except crud.IntegrityError:
        raise HTTPException(status_code=400)

@app.get("/device/")
def get_devices() -> List[ApiTypes.Device]:
    """
    Retrieves all devices.

    Returns:
        List[ApiTypes.Device]: List of devices.

    Raises:
        HTTPException: If no devices are found (status_code=404).
    """
    global crud
    try:
        return crud.get_devices()
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/device/{id}")
def get_device(id):
    """
    Retrieves a device by its ID.

    Args:
        id (int): The ID of the device to retrieve.

    Returns:
        ApiTypes.Device: The device information.

    Raises:
        HTTPException: If the item is not found (status_code=404).
    """
    global crud
    try:
        return crud.get_device(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

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
    """stop the character device reader"""
    global reader
    logger.debug("SHUTDOWN: Sensor reader!")
    reader.stop()
    logger.info("SHUTDOWN: Sensor reader completed!")