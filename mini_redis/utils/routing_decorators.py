# Playing around with some class style of routing using decorators

class Controller:
    __controllers = {}

    @staticmethod
    def get_controllers():
        return Controller.__controllers

    def __init__(self, **kwargs):
        self.__path = kwargs['path']

    def __call__(self, cls):
        if not cls.__name__ in Controller.__controllers:
            Controller.__controllers[cls.__name__] = (cls(), self.__path)
        return Controller.__controllers[cls.__name__][0]

class Route:
    __WRAPPED_METHOD_KEY = "WrappedMethod"

    @staticmethod
    def is_wrapped_method(route_tuple):
        return route_tuple[0] == Route.__WRAPPED_METHOD_KEY

    @staticmethod
    def set_up_route(app, instance, base_path, rt):
        callback = rt[3]
        def _bound_callback(*args, **kwargs):
            return callback(instance, *args, **kwargs)
        app.route(base_path + rt[2], method=[rt[1]], callback=_bound_callback)

    def __init__(self, **kwargs):
        self.__method = kwargs["method"]
        self.__path = kwargs["path"]

    def __call__(self, method):
        return (Route.__WRAPPED_METHOD_KEY, self.__method, self.__path, method)


# binding everything
def register_routes(app):
    instances = Controller.get_controllers()
    for key in instances:
        instance_tuple = instances[key]
        instance, base_path = instance_tuple
        routes_tuples = [rt for rt in [getattr(instance, field, lambda: False) for field in [member for member in dir(instance)]] if isinstance(rt, tuple)]
        for rt in routes_tuples:
            if Route.is_wrapped_method(rt):
                Route.set_up_route(app, instance, base_path, rt)

