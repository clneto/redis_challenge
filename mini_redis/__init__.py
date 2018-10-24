from bottle import Bottle
from .routing_decorators import register_routes
from .controllers import GeneralController

def start_up():
    app = Bottle()
    register_routes(app)
    app.run(host="localhost", port=8080)