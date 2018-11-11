from threading import Thread, Event, Timer, RLock
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

        # timer properties
        self._timer_lock = RLock()
        self._next_trigger_execution = None
        self._trigger_timer = None


    def add_expiration_key(self, key, ttl):
        if ttl != 0:
            trigger_time = (time() + ttl) - self._start_time
            self._queue.put((trigger_time, key))
            self._schedule_trigger(trigger_time)

    def _schedule_trigger(self, time_delta):
        with self._timer_lock:
            if self._next_trigger_execution is None or self._next_trigger_execution > time_delta:
                self._next_trigger_execution = time_delta
                if self._trigger_timer is not None:
                    self._trigger_timer.cancel()

                self._trigger_timer = Timer(time_delta, self._trigger_evaluation)
                self._trigger_timer.start()

    def _trigger_evaluation(self):
        if not self._non_empty_queue.is_set():
            self._non_empty_queue.set()
        with self._timer_lock:
            self._next_trigger_execution = None
            self._trigger_timer = None

    def run(self):
        self._thread.start()

    def stop(self):
        self._keep_processing = False

    def _runStep(self):
        while self._keep_processing:
            self._non_empty_queue.wait() # only process when there is something in queue
            print("looping")
            current_loop_start = time()
            current_time = current_loop_start - self._start_time
            postpone_next_activation = None
            while self._queue.qsize() > 0:
                element = self._queue.get()
                time_delta = element[0] - current_time
                if time_delta < 0: # expired
                    self._expirationHandler(element[1])
                else:
                    self._queue.put(element)
                    if time_delta > 10: ## constant of tolerable active wait
                        postpone_next_activation = time_delta - 1
                    break

            if postpone_next_activation is not None:
                # let's sleep a bit more before evaluating further the queue
                # can be 'preempted' via a new scheduling of trigger
                self._non_empty_queue.clear()
                self._schedule_trigger(postpone_next_activation)

            elif self._queue.qsize() == 0:
                self._non_empty_queue.clear()

            sleep(max([1.0 - (time() - current_loop_start) - 0.0009, 0]))



if __name__ == "__main__":
    ex = ExpirationManager(lambda x : print("Expired: {}".format(x)))
    ex.add_expiration_key("key1", 4)
    ex.add_expiration_key("key2", 3)
    ex.add_expiration_key("key3", 6)
    ex.add_expiration_key("key4", 6)
    ex.run()
    sleep(10)
    ex.add_expiration_key("keyX", 2)
