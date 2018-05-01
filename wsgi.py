#!usr/bin/env python
# -*- coding: utf-8 -*-

# from gevent import monkey

# monkey.patch_all()

import logging
from logging.handlers import RotatingFileHandler

from gevent.wsgi import WSGIServer

from application import create_app

# Failed to find application object 'application' in 'wsgi'
application = create_app()

if __name__ == '__main__':
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler(
        'app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.WARNING)
    handler.setFormatter(formatter)
    application.logger.addHandler(handler)

    http_server = WSGIServer(('', 8080), application)
    http_server.serve_forever()
