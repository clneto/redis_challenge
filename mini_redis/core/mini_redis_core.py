from threading import RLock
from .expiration_manager import ExpirationManager
from .redis_data_store import RedisDataStore
from ..utils import Singleton
from .value_node import ValueNode
from .zset_node import ZSetNode

@Singleton
class MiniRedisCore(RedisDataStore):

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

        value = self._core_data[key].get_value()

        if value is None:
            return "(nil)"
        return value

    def set(self, key, value, ex):
        with self._global_lock:
            if not key in self._core_data:
                node = ValueNode(key, value)
                self._db_size += 1
                self._core_data[key] = node

        self._core_data[key].set_value(value)

        if ex is not None:
            self._expiration_manager.add_expiration_key(key, ex)

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
        with self._global_lock:
            if key not in self._core_data:
                node = ZSetNode()
                self._db_size += 1
                self._core_data[key] = node
            else:
                node = self._core_data[key]

        node.zadd(score, member)
        return "OK"

    def zcard(self, key):
        with self._global_lock:
            node = self._core_data.get(key, None)
        if node is None:
            return "(nil)"
        return node.zcard()

    def zrank(self, key, member):
        with self._global_lock:
            node = self._core_data.get(key, None)
        if node is None:
            return "(nil)"
        return node.zrank(member)

    def zrange(self, key, start, stop):
        with self._global_lock:
            node = self._core_data.get(key, None)
        if node is None:
            return "(nil)"
        return node.zrange(start, stop)
