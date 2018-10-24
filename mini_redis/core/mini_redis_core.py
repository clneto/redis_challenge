from mini_redis.core.redis_data_store import RedisDataStore

class MiniRedisCore(RedisDataStore):

    class DataNode:
        def __init__(self, key, value):
            self.lock = {}
            self.value = value
            self.key = key

        def setValue(self, value):
            # acquire lock
            self.value = value
            # release lock

        def getValue(self):
            # acquire lock
            value = self.value
            # release lock
            return value

        def incr(self):
            # acquire lock
            value = self.value+1
            # release lock
            return value


    db_size = 0
    core_data = {}

    def dbsize(self):
        return MiniRedisCore.db_size

    def get(self, key):
        # check if not changing maybe / particular lock or event-lock here
        # lock
        if key not in MiniRedisCore.core_data:
            return "(nil)"
        # release

        value = MiniRedisCore.core_data[key].getValue()

        if value is None:
            pass #fail gracefully
        return value

    def set(self, key, value, ex):
        if not key in MiniRedisCore.core_data:
            nodeValue = MiniRedisCore.DataNode(key, value)
            # size lock ~ rlock
            MiniRedisCore.db_size += 1
            MiniRedisCore.core_data[key] = nodeValue
            # release lock

        MiniRedisCore.core_data[key].setValue(value)

        if ex is not None:
            pass #schedule eviction

        return "OK"


    def incr(self, key):
        if key in MiniRedisCore.core_data:
            return MiniRedisCore.core_data[key].incr()
        return "" # failure

    def delete(self, key):
        pass

    def zadd(self, key, score, member):
        pass

    def zcard(self, key):
        pass

    def zrank(self, key, member):
        pass

    def zrange(self, key, start, stop):
        pass
