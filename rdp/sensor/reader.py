import logging
import struct
import threading
import time
import random

from rdp.crud import Crud

logger = logging.getLogger("rdp.sensor")


class Reader:
    def __init__(self, crud: Crud, device: str = "/dev/rdp_cdev"):
        self._crud = crud
        self._device = device
        self._thread: threading.Thread = None

    def start(self) -> None:
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def stop(self):
        thread = self._thread
        self._thread = None
        thread.join()

    def _run(self) -> None:
        count = 0

        # Testdaten für location
        self._crud.add_location(location_name="Location_1", city="City_1")
        self._crud.add_location(location_name="Location_2", city="City_2")
        self._crud.add_location(location_name="Location_3", city="City_3")

        # Testdaten für room
        self._crud.add_room(room_name="Room_1", room_nr=101, location_id=1)
        self._crud.add_room(room_name="Room_2", room_nr=102, location_id=2)
        self._crud.add_room(room_name="Room_3", room_nr=103, location_id=3)

        # Testdaten für device
        self._crud.add_device(
            device_device="Device_1",
            device_name="Device_1",
            postalCode=12345,
            city="City_1",
            room_id=1,
        )
        self._crud.add_device(
            device_device="Device_2",
            device_name="Device_2",
            postalCode=54321,
            city="City_2",
            room_id=2,
        )
        self._crud.add_device(
            device_device="Device_3",
            device_name="Device_3",
            postalCode=67890,
            city="City_3",
            room_id=3,
        )
        
        while self._thread is not None:
            logger.info("A")
            with open("/dev/rdp_cdev", "rb") as f:
                test = f.read(16)
                for i in range(16):
                    if i % 2:
                        print("  ", end="")
                value_time = 0
                for i in range(8):
                    value_time |= test[i] << 8 * i
                type_num = 0
                for i in range(4):
                    type_num |= test[i + 8] << 8 * i
                value = 0.0
                value = struct.unpack("f", test[-4::])
                logger.debug(
                    "Read one time: %d type :%d and value %f",
                    value_time,
                    type_num,
                    value[0],
                )
                try:
                    self._crud.add_value(value_time, type_num, random.randint(1, 3), value[0]) #random.randint() --> weist random id von device zu value
                except self._crud.IntegrityError:
                    logger.info("All Values read")
                    break
            time.sleep(0.1)
            count += 1
            if count % 100 == 0:
                logger.info("read 100 values")
                count = 0