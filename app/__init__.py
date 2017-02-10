'''
Assemble our service.
'''
import config
from flask import Flask
import logging

def _initialize_blueprints(application):
    '''
    Register Flask blueprints
    '''
    from app.views.datadog import datadog
    application.register_blueprint(datadog, url_prefix='/api/v1/datadog')

def _initialize_errorhandlers(application):
    '''
    Initialize error handlers
    '''
    from app.errors import errors
    application.register_blueprint(errors)

def _initialize_logging(application):
    # We only configure the root logger in our setup.  Flask already provides
    # us with the app logger.  We don't mess with it's name as we do in other
    # apps because we can use `_logger = logging.getLogger(__name__)` at the
    # top of every file where we want a logger.
    formatter = logging.Formatter(config.LOG_FORMAT)

    root_logger = logging.getLogger('')
    root_logger.setLevel(config.LOG_LEVEL)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(config.LOG_LEVEL)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)


def create_app():
    '''
    Create an app by initializing components.
    '''
    application = Flask(__name__)

    _initialize_logging(application)
    _initialize_errorhandlers(application)
    _initialize_blueprints(application)

    # Do it!
    return application

