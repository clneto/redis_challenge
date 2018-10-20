from bottle import route, run

from routes import *

run(host="localhost", port=8080, debug=True)