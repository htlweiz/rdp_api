import threading
import time
import logging
import struct


FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
LOGGER_TO_USE="rdp.sensor"
logger=logging.getLogger(LOGGER_TO_USE)

class Reader:
    def __init__(self, crud, device="/dev/rdp_cdev"):
        self._crud=crud
        self._device=device
        self._thread=None

    def start(self):
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def stop(self):
        thread=self._thread
        self._thread=None
        thread.join() 

    def _run(self):
        count=0
        while self._thread is not None:
            logger.info("A")
            with open("/dev/rdp_cdev","rb") as f:
                print("Yes it's open")
                test = f.read(16)
                for i in range(16):
                    print("%.2X"%test[i],end=" ")
                    if (i%2):
                        print("  ", end="")
                value_time = 0
                for i in range(8):
                    value_time |= test[i] << 8*i
                type_num = 0
                for i in range(4):
                    type_num |= test[i+8] << 8*i
                value = 0.0
                print()
                print (test[-4::])
                value=struct.unpack('f',test[-4::])
                # for i in range(4):
                #     value |= test[i+12] << 8*i
                print()
                print(value)
                print("Read one time: %d type :%d and value %f" % (value_time,type_num,value[0]))
                try:
                    self._crud.add_value(value_time,type_num, value[0])     
                except self._crud.IntegrityError:
                    logger.info("All Values read")
                    break
            time.sleep(0.1)
            count+=1
            if count % 100 == 0:
                logger.info("read 100 values")
                count=0


