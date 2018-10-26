from mini_redis.core.redis_data_store import RedisDataStore
from threading import RLock
from .expiration_manager import ExpirationManager
from mini_redis.utils import Singleton

@Singleton
class MiniRedisCore(RedisDataStore):

    class DataNode:
        def __init__(self, key, value):
            self.lock = RLock()
            self.value = value
            self.key = key

        def setValue(self, value):
            with self.lock:
                self.value = value


        def getValue(self):
            with self.lock:
                value = self.value
            return str(value)

        def incr(self):
            with self.lock:
                self.value += 1
            return "OK"

    def __init__(self):
        self._global_lock = RLock()
        self._db_size = 0
        self._core_data = {}
        self._expiration_manager = ExpirationManager(self.delete)
        self._expiration_manager.run()

    def dbsize(self):
        return str(self._db_size)

    def get(self, key):
        # check if not changing maybe / particular lock or event-lock here
        with self._global_lock:
            if key not in self._core_data:
                return "(nil)"

        value = self._core_data[key].getValue()

        if value is None:
            return "(nil)"
        return value

    def set(self, key, value, ex):
        with self._global_lock:
            if not key in self._core_data:
                nodeValue = self.DataNode(key, value)
                self._db_size += 1
                self._core_data[key] = nodeValue

        self._core_data[key].setValue(value)

        if ex is not None:
            self._expiration_manager.addExpirationKey(key, ex)

        return "OK"


    def incr(self, key):
        node = None
        with self._global_lock:
            if key in self._core_data:
                node = self._core_data[key]

        if node is not None:
            return node.incr()
        return "(nil)" # failure

    def delete(self, key):
        with self._global_lock:
            if key in self._core_data:
                del self._core_data[key]
                return "OK"
        return "(nil)"

    def zadd(self, key, score, member):
        pass

    def zcard(self, key):
        pass

    def zrank(self, key, member):
        pass

    def zrange(self, key, start, stop):
        pass
