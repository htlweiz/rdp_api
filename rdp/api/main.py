from typing import Union, List, Annotated

from fastapi import FastAPI, HTTPException, UploadFile, Form

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
        crud.update_device(
            id, device_device=device.name, device_name=device.name, postalCode=device.postalCode, city=device.city, room_id=device.room_id
        )
        return get_device(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")
    except crud.IntegrityError:
        raise HTTPException(status_code=400)


@app.get("/device/")
def get_devices() -> List[ApiTypes.Device]:
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


@app.get("/room/{id}")
def get_room(id) -> ApiTypes.Room:
    """
    Retrieve a room by ID.

    Args:
        id: The ID of the room to retrieve.

    Returns:
        ApiTypes.Room: The room object.
        
    Raises:
        HTTPException: If the room is not found (status code 404).
    """
    global crud
    try:
        return crud.get_room(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/room/")
def get_rooms() -> List[ApiTypes.Room]:
    """
    Retrieve all rooms.

    Returns:
        List[ApiTypes.Room]: A list of room objects.
        
    Raises:
        HTTPException: If no rooms are found (status code 404).
    """
    global crud
    try:
        return crud.get_rooms()
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.put("/room/{id}/")
def put_room(id, room: ApiTypes.RoomNoID) -> ApiTypes.Room:
    """
    Update or create a room.

    Args:
        id: The ID of the room to update/create.
        room: The room data.

    Returns:
        ApiTypes.Room: The updated/created room object.
        
    Raises:
        HTTPException: If the room is not found (status code 404) or an integrity error occurs (status code 400).
    """
    global crud
    try:
        room = crud.update_room(id, room_name=room.name, room_nr=room.room_nr, location_id=room.location_id)
        return get_room(room.id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")
    except crud.IntegrityError as e:
        raise HTTPException(
            status_code=400,
        )

@app.get("/location/{id}")
def get_location(id) -> ApiTypes.Location:
    """
    Retrieve location by ID.

    Args:
        id (int): The unique identifier for the location.

    Returns:
        ApiTypes.Location: The location details for the specified ID.

    Raises:
        HTTPException: If the item is not found (status code 404).
    """
    global crud
    try:
        return crud.get_location(id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/location/")
def get_locations() -> List[ApiTypes.Location]:
    """
    Retrieve all locations.

    Returns:
        List[ApiTypes.Location]: List of all locations.

    Raises:
        HTTPException: If no items are found (status code 404).
    """
    global crud
    try:
        return crud.get_locations()
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

@app.put("/location/{id}/")
def put_location(id, location: ApiTypes.LocationNoId) -> ApiTypes.Location:
    """
    Update or add a location by ID.

    Args:
        id (int): The unique identifier for the location.
        location (ApiTypes.LocationNoId): The location details without ID.

    Returns:
        ApiTypes.Location: The updated or newly added location details.

    Raises:
        HTTPException: If the item is not found (status code 404) or if an integrity error occurs (status code 400).
    """
    global crud
    try:
        location = crud.update_location(id, location_name=location.name, city=location.city)
        return get_location(location.id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")
    except crud.IntegrityError as e:
        raise HTTPException(
            status_code=400,
        )

#Post
@app.post("/location/")
def post_location(location: ApiTypes.LocationNoId) -> ApiTypes.Location:
    """
    Add a new location.

    Args:
        location (ApiTypes.LocationNoId): The location details without ID.

    Returns:
        ApiTypes.Location: The newly added location details.

    Raises:
        HTTPException: If an integrity error occurs (status code 400).
    """
    global crud
    try:
        location = crud.add_location(location_name=location.name, city=location.city)
        return get_location(location.id)
    except crud.IntegrityError as e:
        raise HTTPException(status_code=400)


@app.post("/device/")
def post_device(device: ApiTypes.DeviceNoID) -> ApiTypes.Device:
    """
    Add a new device.

    Args:
        device (ApiTypes.DeviceNoID): The device details without ID.

    Returns:
        ApiTypes.Device: The newly added device details.

    Raises:
        HTTPException: If an integrity error occurs (status code 400).
    """
    global crud
    try:
        new_device = crud.add_device(
            device_device=device.name,
            device_name=device.name,
            postalCode=device.postalCode,
            city=device.city,
            room_id=device.room_id
        )
        return new_device
    except crud.IntegrityError as e:
        raise HTTPException(status_code=400)


@app.post("/room/")
def post_room(room: ApiTypes.RoomNoID) -> ApiTypes.Room:
    """
    Create a new room.

    Args:
        room: The room data.

    Returns:
        ApiTypes.Room: The newly created room object.
        
    Raises:
        HTTPException: If an integrity error occurs (status code 400).
    """
    global crud
    try:
        new_room = crud.add_room(
            room_name=room.name,
            room_nr=room.room_nr,
            location_id=room.location_id
        )
        return new_room
    except crud.IntegrityError as e:
        raise HTTPException(status_code=400)

# Get Value by device_id
@app.get("/value/{device_id}")
def get_values_by_device_id(device_id: int) -> List[ApiTypes.Value]:
    """
    Get values by device ID.

    Args:
        device_id (int): The ID of the device.

    Returns:
        List[ApiTypes.Value]: A list of values associated with the device.

    Raises:
        HTTPException: If the device is not found (status code 404) or an integrity error occurs (status code 400).
    """
    global crud
    try:
        return crud.get_value_by_device_id(device_id)
    except crud.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")
    except crud.IntegrityError as e:
        raise HTTPException(
            status_code=400,
        )


@app.post("/value/")
def post_new_value(value_time: int, value_type_id: int, device_id: int, value_value: float) -> None:
    """
    Create a new value.

    Args:
        value_time: The value time.
        value_type_id: The ID of value_type.
        device_id: The ID of device.
        value_value: The value

    Returns:
        ApiTypes.Room: The newly created room object.
        
    Raises:
        HTTPException: If an integrity error occurs (status code 400).
    """
    global crud
    try:
        crud.add_new_value(value_time, value_type_id, device_id, value_value)
    except IntegrityError:
        raise HTTPException(status_code=500, detail="Integrity error while adding new value")

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