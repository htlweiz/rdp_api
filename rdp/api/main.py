import logging
from typing import List, Annotated

from fastapi import FastAPI, HTTPException, UploadFile, Form
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


@app.post("/device/")
def post_device(device: ApiTypes.DeviceNoID) -> ApiTypes.Device:
    """PUT device: Add device.

    Args:
        device (ApiTypes.DeviceNoID): json object representing the new state of the device.

    Raises:
        HTTPException

    Returns:
        ApiTypes.Device: A device in the database.

    """
    global crud
    try:
        return crud.add_or_update_device(
            device_device=device.device, device_name=device.name
        )
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")
    except crud.IntegrityError:
        raise HTTPException(
            status_code=400,
        )


@app.put("/device/{id}/")
def put_device(id, device: ApiTypes.DeviceNoID) -> ApiTypes.Device:
    """PUT device: Update device of id.

    Args:
        id int: device id
        device (ApiTypes.DeviceNoID): json object representing the new state of the device.

    Raises:
        HTTPException

    Returns:
        ApiTypes.Device: A device in the database.

    """
    global crud
    try:
        return crud.add_or_update_device(
            id, device_device=device.device, device_name=device.name
        )
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")
    except crud.IntegrityError:
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


@app.get("/room/")
def get_rooms(room_group_id: int = None) -> List[ApiTypes.Room]:
    """Get rooms from the database.
    Args:
        room_group_id int: room group id to find all rooms that are children from this group.

    Raises:
        HTTPException

    Returns:
        List[ApiTypes.Room]: A list of rooms in the database.
    """
    global crud
    try:
        return crud.get_rooms(room_group_id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")


@app.post("/room/")
def post_room(room: ApiTypes.RoomNoID) -> ApiTypes.Room:
    """POST room: Add room.

    Args:
        room (ApiTypes.RoomNoID): json object representing the new state of the room.

    Raises:
        HTTPException

    Returns:
        ApiTypes.Room: A room in the database.

    """
    global crud
    try:
        return crud.add_or_update_room(
            room_name=room.name, room_group_id=room.room_group_id
        )
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")
    except crud.IntegrityError:
        raise HTTPException(
            status_code=400,
        )


@app.put("/room/{id}/")
def put_room(id: int, room: ApiTypes.RoomNoID) -> ApiTypes.Room:
    """PUT room: Update room of id.

    Args:
        id int: room id
        room (ApiTypes.RoomNoID): json object representing the new state of the room.

    Raises:
        HTTPException

    Returns:
        ApiTypes.Room: A room in the database.

    """
    global crud
    try:
        return crud.add_or_update_room(
            id, room_name=room.name, room_group_id=room.room_group_id
        )
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")
    except crud.IntegrityError:
        raise HTTPException(
            status_code=400,
        )


@app.get("/room-group/{id}")
def get_room_group(id) -> ApiTypes.RoomGroup:
    """Get specific room group from the database with the specified id.
    Args:
        id int: room group id

    Raises:
        HTTPException

    Returns:
        ApiTypes.RoomGroup: A room group in the database.
    """
    global crud
    try:
        return crud.get_room_group(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/room-group/")
def get_room_groups() -> List[ApiTypes.RoomGroup]:
    """Get all room groups from the database.

    Raises:
        HTTPException

    Returns:
        List[ApiTypes.RoomGroup]: List of all room groups in the database.
    """
    global crud
    try:
        return crud.get_room_groups()
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")


@app.post("/room-group/")
def post_room_group(room_group: ApiTypes.RoomGroupNoID) -> ApiTypes.RoomGroup:
    """POST room group: Add room group.

    Args:
        room_group (ApiTypes.RoomGroupNoID): json object representing the new state of the room group.

    Raises:
        HTTPException

    Returns:
        ApiTypes.RoomGroup: A room group in the database.

    """
    global crud
    try:
        return crud.add_or_update_room_group(
            room_group_name=room_group.name, parent_group_id=room_group.room_group_id
        )
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")
    except crud.IntegrityError:
        raise HTTPException(
            status_code=400,
        )


@app.put("/room-group/{id}/")
def put_room_group(id: int, room_group: ApiTypes.RoomGroupNoID) -> ApiTypes.RoomGroup:
    """PUT room group: Update room group of id.

    Args:
        id int: room id
        room_group (ApiTypes.RoomGroupNoID): json object representing the new state of the room group.

    Raises:
        HTTPException

    Returns:
        ApiTypes.RoomGroup: A room group in the database.

    """
    global crud
    try:
        return crud.add_or_update_room_group(
            id,
            room_group_name=room_group.name,
            parent_group_id=room_group.room_group_id,
        )
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")
    except crud.IntegrityError:
        raise HTTPException(
            status_code=400,
        )


@app.post("/csv/")
async def upload_csv_files(
    file: UploadFile,
    device_id: Annotated[int, Form()],
):
    """POST value data

    Args:
        file: File in csv format
        device_id: device id

    Returns:
        success
    """
    global crud
    try:
        crud.load_csv(await file.read(), device_id)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
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
