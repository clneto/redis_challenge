from bottle import get

@get('/healthcheck')
def health_check_route():
    return {"status": "Im Fine!"}