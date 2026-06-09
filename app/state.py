from threading import Lock


class AppState:
    def __init__(self):
        self.users = 0
        self.orders = 0
        self.errors = 0
        self.queue_size = 0

        self.cpu_attack = False
        self.memory_attack = False
        self.error_mode = False

        self.memory_storage = []
        self.lock = Lock()


state = AppState()