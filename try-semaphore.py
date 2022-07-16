from PyQt5.QtCore import QSystemSemaphore, QSharedMemory

class SharedMemory(object):

    NAME = "mu-memory"

    def __init__(self):
        self._shared_memory = QSharedMemory(self.NAME)

    def __enter__(self):
        self._shared_memory.lock()
        return self._shared_memory

    def __exit__(self, *args, **kwargs):
        self._shared_memory.unlock()

with SharedMemory() as shared_memory:
    if shared_memory.attach():
        print("Attached; already running")
        is_running = True
    else:
        shared_memory.create(1)
        is_running = False

if is_running:  # if the application is already running, show the warning message
    raise RuntimeError("Already running")
else:
    print("Not running")

input("Press enter...")