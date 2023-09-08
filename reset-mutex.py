import struct
from PyQt5.QtCore import (
    Qt,
    QEventLoop,
    QThread,
    QObject,
    pyqtSignal,
    QSharedMemory,
)

shm = QSharedMemory("mu-tex")
shm.lock()
try:
    if shm.attach():
        print("Able to attach")
    else:
        print("Unable to attach")
    data = shm.data()
    print(data)
    if data:
        print(list(data))
        print(struct.unpack("q", data[:8]))
    else:
        print("No data")
    shm.detach()
finally:
    shm.unlock()
