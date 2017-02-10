'''
DataDog Model
'''
from app.errors import AppBaseError
import config
import logging

_logger = logging.getLogger(__name__)

DATADOG_API_KEY = config.DATADOG_API_KEY
DATADOG_APP_KEY = config.DATADOG_APP_KEY

class DataDogBaseError(AppBaseError):
    '''
    Base DataDog error.
    '''

class DataDogModel:
    def __init__(self, api_key=DATADOG_API_KEY, app_key=DATADOG_APP_KEY):
        pass

    def is_available(self):
        '''
        Check ability to access DataDog.
        '''

        return True

    def put_alert_data(self, alert):
        '''
        Put alert data into DataDog.
        '''

        return None

