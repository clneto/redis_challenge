from abc import ABC, abstractmethod


class RedisDataStore(ABC):

    @abstractmethod
    def dbsize(self):
        pass

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, key, value, ex):
        pass

    @abstractmethod
    def incr(self, key):
        pass

    @abstractmethod
    def zadd(self, key, score, member):
        pass

    @abstractmethod
    def zcard(self, key):
        pass

    @abstractmethod
    def zrank(self, key, member):
        pass

    @abstractmethod
    def zrange(self, key, start, stop):
        pass

    @abstractmethod
    def delete(self, key):
        pass

