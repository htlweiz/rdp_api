import logging
from typing import List

from fastapi import FastAPI, HTTPException, UploadFile
from rdp.crud import Crud, create_engine
from rdp.sensor import Reader

from . import api_types as ApiTypes

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


@app.get("/device/{id}")
def get_device(id) -> ApiTypes.Device:
    """Get specific device from the database with the specified id.
    Args:
        id int: device id

    Raises:
        HTTPException

    Returns:
        ApiTypes.Device: A device in the database.
    """
    global crud
    try:
        return crud.get_device(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")


@app.put("/device/{id}/")
def put_device(id, device: ApiTypes.DeviceNoID) -> ApiTypes.Device:
    """PUT device: Add device or update device of id.

    Args:
        id int: device id

    Raises:
        HTTPException

    Returns:
        ApiTypes.Device: A device in the database.

    """
    global crud
    try:
        device = crud.add_or_update_device(
            id, device_device=device.device, device_name=device.name
        )
        return get_device(device.id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")
    except crud.IntegrityError as e:
        raise HTTPException(
            status_code=400,
        )


@app.get("/device/")
def get_devices() -> List[ApiTypes.Device]:
    """Get all devices from the database.
    Raises:
        HTTPException

    Returns:
        List[ApiTypes.Device]: A list of all devices stored in the database.
    """
    global crud
    try:
        return crud.get_devices()
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/value/")
def get_values(
    type_id: int = None, start: int = None, end: int = None, device: int = None
) -> List[ApiTypes.Value]:
    """Get values from the database. The default is to return all available values. This result can be filtered.

    Args:
        type_id (int, optional): If set, only values of this type are returned. Defaults to None.
        start (int, optional): If set, only values at least as new are returned. Defaults to None.
        end (int, optional): If set, only values not newer than this are returned. Defaults to None.
        end (int, optional): If set, only values of specified device are returned. Defaults to None.

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


@app.get("/room/{id}")
def get_room(id) -> ApiTypes.Room:
    """Get specific room from the database with the specified id.
    Args:
        id int: room id

    Raises:
        HTTPException

    Returns:
        ApiTypes.Room: A room in the database.
    """
    global crud
    try:
        return crud.get_room(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")


@app.put("/room/{id}/")
def put_room(id, device: ApiTypes.RoomNoID) -> ApiTypes.Room:
    """PUT room: Add room or update room of id.

    Args:
        id int: room id

    Raises:
        HTTPException

    Returns:
        ApiTypes.Room: A room in the database.

    """
    global crud
    try:
        room = crud.add_or_update_room(id, room_name=device.name)
        return get_room(room.id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")
    except crud.IntegrityError as e:
        raise HTTPException(
            status_code=400,
        )


@app.post("/csv/")
async def upload_csv_files(file: UploadFile):
    global crud
    logger.error("csvfile")
    crud.load_csv(await file.read())
    return {"detail": "success"}


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
