from threading import Thread, Event
from queue import PriorityQueue
from time import time, sleep

global_time = time()

class ExpirationManager:

    def __init__(self, expirationHandler):
        self._non_empty_queue = Event()
        self._queue = PriorityQueue()
        self._expirationHandler = expirationHandler
        self._thread = Thread(name="Expiration-Manager", target=self._runStep)
        self._keep_processing = True
        self._start_time = time()

    def addExpirationKey(self, key, ttl):
        if ttl != 0:
            self._queue.put(((time() + ttl) - self._start_time, key))
            if not self._non_empty_queue.is_set():
                self._non_empty_queue.set()

    def run(self):
        self._thread.start()

    def stop(self):
        self._keep_processing = False

    def _runStep(self):
        while self._keep_processing:
            self._non_empty_queue.wait() # only process when there is something in queue
            current_loop_start = time()
            current_time = current_loop_start - self._start_time
            keep_consuming = True
            while self._queue.qsize() > 0 and keep_consuming:
                element = self._queue.get()
                if element[0] < current_time:
                    self._expirationHandler(element[1])
                else:
                    self._queue.put(element)
                    keep_consuming = False
            if keep_consuming: # queue is empty
                self._non_empty_queue.clear()
            sleep(max([1.0 - (time() - current_loop_start) - 0.0009, 0]))



if __name__ == "__main__":
    ex = ExpirationManager(lambda x : print("Expired: {}".format(x)))
    ex.addExpirationKey("key1", 4)
    ex.addExpirationKey("key2", 3)
    ex.addExpirationKey("key3", 6)
    ex.addExpirationKey("key4", 6)
    ex.run()
    sleep(10)
    ex.addExpirationKey("keyX", 2)
