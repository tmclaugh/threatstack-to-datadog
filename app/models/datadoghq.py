'''
DataDog Model
'''
from app.errors import AppBaseError
import config
import datadog
import logging

_logger = logging.getLogger(__name__)

DATADOG_API_KEY = config.DATADOG_API_KEY
DATADOG_APP_KEY = config.DATADOG_APP_KEY

THREATSTACK_TO_DATADOG_ALERTS = {
    1: 'error',
    2: 'warning',
    3: 'info'
}

class DataDogBaseError(AppBaseError):
    '''
    Base DataDog error.
    '''

class DataDogModel:
    def __init__(self, api_key=DATADOG_API_KEY, app_key=DATADOG_APP_KEY):
        datadog.initialize(api_key=api_key, app_key=app_key)

    def is_available(self):
        '''
        Check ability to access DataDog.
        '''

        return True

    def put_alert_event(self, alert, hostname=None):
        '''
        Put alert data into DataDog.
        '''

        event = {}
        event['title'] = 'Threat Stack alert: {}'.format(alert.get('rule').get('original_rule').get('name'))
        event['text'] = alert.get('title')
        event['host'] = hostname
        event['source_type_name'] = 'threatstack'
        event['date_happened'] = int(alert.get('created_at') / 1000)

        ts_severity = alert.get('severity')
        event['alert_type'] = THREATSTACK_TO_DATADOG_ALERTS[ts_severity]
        if ts_severity < 3:
            priority = 'normal'
        else:
            priority = 'low'
        event['priority'] = priority

        response = datadog.api.Event.create(**event)
        return response

