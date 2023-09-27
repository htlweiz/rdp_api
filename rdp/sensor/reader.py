import logging
import struct
import threading
import time

from rdp.crud import Crud

logger = logging.getLogger("rdp.sensor")


class Reader:
    def __init__(self, crud: Crud, device: str = "/dev/rdp_cdev"):
        self._crud = crud
        self._thread: threading.Thread = None
        try:
            crud.add_or_update_device(None, device_device=device, device_name="default_device")
        except crud.IntegrityError:
            pass
        self._devices = []

    def start(self) -> None:
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def stop(self):
        thread = self._thread
        self._thread = None
        thread.join()

    def _run(self) -> None:
        count = 0
        while self._thread is not None:
            self._devices = self._crud.get_devices()
            logger.info("A")
            for device in self._devices:
                with open(device.device, "rb") as f:
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
                        self._crud.add_value(value_time, type_num, device.id, value[0])
                    except self._crud.IntegrityError:
                        logger.info("All Values read")
                        break
            time.sleep(0.1)
            count += 1
            if count % 100 == 0:
                logger.info("read 100 values")
                count = 0
