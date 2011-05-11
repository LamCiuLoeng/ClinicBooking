# -*- coding: utf-8 -*-
from flup.server.fcgi import WSGIServer
from sys2do import app


if __name__ == '__main__':
#    app.run(host = '127.0.0.1', port = 8888)
    WSGIServer(app, bindAddress = ("localhost", 8001)).run()
