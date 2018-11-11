from mini_redis.core.mini_redis_core import MiniRedisCore

def set_handler(cmdRequest, mini_redis):
    return mini_redis.set(cmdRequest.get("key", None), cmdRequest.get("value", None), cmdRequest.get("ex", None))

def get_handler(cmdRequest, mini_redis):
    return mini_redis.get(cmdRequest.get("key", None))

def del_handler(cmdRequest, mini_redis):
    return mini_redis.delete(cmdRequest.get("key", None))

def dbsize_handler(_, mini_redis):
    return mini_redis.dbsize()

def incr_handler(cmdRequest, mini_redis):
    return mini_redis.incr(cmdRequest.get("key", None))

def zadd_handler(cmdRequest, mini_redis):
    return mini_redis.zadd(cmdRequest.get("key", None), cmdRequest.get("score", None), cmdRequest.get("member", None))

def zcard_handler(cmdRequest, mini_redis):
    return mini_redis.zcard(cmdRequest.get("key", None))

def zrank_handler(cmdRequest, mini_redis):
    return mini_redis.zrank(cmdRequest.get("key", None), cmdRequest.get("member", None))

def zrange_handler(cmdRequest, mini_redis):
    return mini_redis.zrange(cmdRequest.get("key", None), cmdRequest.get("start", None), cmdRequest.get("stop", None))

class CmdHandlerService:

    mini_redis = MiniRedisCore()

    def __init__(self):
        self.cmd_handler = {}
        self.cmd_handler["set"] = set_handler
        self.cmd_handler["get"] = get_handler
        self.cmd_handler["del"] = del_handler
        self.cmd_handler["dbsize"] = dbsize_handler
        self.cmd_handler["incr"] = incr_handler
        self.cmd_handler["zadd"] = zadd_handler
        self.cmd_handler["zcard"] = zcard_handler
        self.cmd_handler["zrank"] = zrank_handler
        self.cmd_handler["zrange"] = zrange_handler


    def processCmd(self, cmdRequest):
        cmd = cmdRequest.get("cmd", None)
        if cmd is None:
            return "Missing command"
        cmd = cmd.lower()
        handler = self.cmd_handler[cmd]
        if handler is None:
            return "Yet unsupported command"
        return handler(cmdRequest, CmdHandlerService.mini_redis)