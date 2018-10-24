from mini_redis.core.mini_redis_core import MiniRedisCore

def safe_get(obj, field):
    if field in obj:
        return obj[field]
    return None

def set_handler(cmdRequest, mini_redis):
    mini_redis.set(safe_get(cmdRequest, "key"),
                   safe_get(cmdRequest, "value"),
                   safe_get(cmdRequest, "ex"))

def get_handler(cmdRequest, mini_redis):
    mini_redis.get(safe_get(cmdRequest, "key"))

def del_handler(cmdRequest, mini_redis):
    mini_redis.delete(safe_get(cmdRequest, "key"))

def dbsize_handler(cmdRequest, mini_redis):
    return mini_redis.dbsize()

def incr_handler(cmdRequest, mini_redis):
    mini_redis.incr(safe_get(cmdRequest, "key"))


class CmdHandlerService:

    mini_redis = MiniRedisCore()

    def __init__(self):
        self.cmd_handler = {}
        self.cmd_handler["set"] = set_handler
        self.cmd_handler["get"] = get_handler
        self.cmd_handler["del"] = del_handler
        self.cmd_handler["dbsize"] = dbsize_handler
        self.cmd_handler["incr"] = incr_handler


    def processCmd(self, cmdRequest):
        handler = self.cmd_handler[cmdRequest.cmd]
        if handler is None:
            return "Yet unsupported command"

        return handler(cmdRequest.cmd, CmdHandlerService.mini_redis)