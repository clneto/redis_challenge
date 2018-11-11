from threading import RLock

class ValueNode:
    def __init__(self, key, value):
        self.lock = RLock()
        self.value = value
        self.key = key

    def set_value(self, value):
        with self.lock:
            self.value = value

    def get_value(self):
        with self.lock:
            value = self.value
        return str(value)

    def incr(self):
        with self.lock:
            self.value += 1
        return "OK"