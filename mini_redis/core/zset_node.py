from threading import RLock
from .sorted_structures import AVLTree

class ZSetNode:

    def __init__(self):
        self._lock = RLock()
        self._count = 0
        self._member_to_score = {}
        self._tree_values = AVLTree()

    def zadd(self, score, value):
        member_key = hash(value)
        cast_score = int(score)
        with self._lock:
            if member_key not in self._member_to_score:
                self._count += 1
            self._member_to_score[member_key] = cast_score
            self._tree_values.add_value(cast_score, value)

    def zcard(self):
        with self._lock:
            return self._count

    def zrank(self, member):
        with self._lock:
            score = self._member_to_score.get(hash(member), None)
            if score is None:
                return "(nil)"
            return self._tree_values.get_rank(score)

    def zrange(self, start, stop):
        with self._lock:
            return self._tree_values.get_range(int(start), int(stop))
