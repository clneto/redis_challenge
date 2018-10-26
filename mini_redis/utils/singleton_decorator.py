class Singleton:
    __instances = {}

    def __init__(self, klass):
        self._class = klass

    def __call__(self, *args, **kwargs):
        if not self._class.__name__ in Singleton.__instances:
            Singleton.__instances[self._class.__name__] = self._class(*args, **kwargs)
        return Singleton.__instances[self._class.__name__]