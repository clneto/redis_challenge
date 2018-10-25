from mini_redis.routing_decorators import Controller, Route
from mini_redis.services import CmdHandlerService
from bottle import request

from threading import current_thread

@Controller(path="/")
class GeneralController:

    def __init__(self):
        self.cmd_handler = CmdHandlerService()

    @Route(method="POST", path="cmd")
    def processCmd(self):
        return self.cmd_handler.processCmd(request.json)

    @Route(method="GET", path="healthcheck")
    def getHealthcheck(self):
        return {"status": "Im Fine!", "from": current_thread().ident}

    @Route(method="GET", path="echo/<param>")
    def getEcho(self, param):
        return "echo {}".format(param)

    @Route(method="PUT", path="echo")
    def putEcho(self):
        return "echo {}".format(request.body.read().decode("utf-8"))




