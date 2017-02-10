#!/usr/bin/env python

from app import create_app
import logging
from logging.config import fileConfig

fileConfig('logging.conf', disable_existing_loggers=False)
_logger = logging.getLogger(__name__)

# Gunicorn entry point.
application = create_app()

if __name__ == '__main__':
    # Entry point when run via Python interpreter.
    _logger.info("== Running in debug mode ==")
    application.run(host='localhost', port=8080, debug=True)
