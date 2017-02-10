'''
Communicate with Threat Stack
'''
import config
import requests
import six
import sys
from app.errors import AppBaseError

THREATSTACK_API_KEY = config.THREATSTACK_API_KEY
THREATSTACK_BASE_URL = config.THREATSTACK_BASE_URL

class ThreatStackBaseError(AppBaseError):
    '''
    Base Threat Stack error.
    '''

class ThreatStackRequestError(ThreatStackBaseError):
    '''
    Base Threat Stack error.
    '''

class ThreatStackAPIError(ThreatStackBaseError):
    '''
    Base Threat Stack error.
    '''

class ThreatStackModel:
    def __init__(self):
        '''
        Interact with Threat Stack via API.
        '''

    def is_available(self):
        '''
        Check connectivity to Threat Stack.

        Returns a failure if cannot connect to Threat Stack API.  This could be
        anything from API credential issues to connection failure.
        '''

        alerts_url = '{}/alerts?count=1'.format(THREATSTACK_BASE_URL)

        try:
            resp = requests.get(
                alerts_url,
                headers={'Authorization': THREATSTACK_API_KEY}
            )

        except requests.exceptions.RequestException as e:
            exc_info = sys.exc_info()
            if sys.version_info >= (3,0,0):
                raise ThreatStackRequestError(e).with_traceback(exc_info[2])
            else:
                six.reraise(
                    ThreatStackRequestError,
                    ThreatStackRequestError(e),
                    exc_info[2]
                )

        if not resp.ok:
            if 'application/json' in resp.headers.get('Content-Type'):
                raise ThreatStackAPIError(
                    resp.reason,
                    resp.status_code,
                    resp.json()
                )
            else:
                raise ThreatStackRequestError(resp.reason, resp.status_code)

        return True

    def get_alert_by_id(self, alert_id):
        '''
        Retrieve an alert from Threat Stack by alert ID.
        '''
        alerts_url = '{}/alerts/{}'.format(THREATSTACK_BASE_URL, alert_id)

        try:
            resp = requests.get(
                alerts_url,
                headers={'Authorization': THREATSTACK_API_KEY}
            )

        except requests.exceptions.RequestException as e:
            exc_info = sys.exc_info()
            if sys.version_info >= (3,0,0):
                raise ThreatStackRequestError(e).with_traceback(exc_info[2])
            else:
                six.reraise(
                    ThreatStackRequestError,
                    ThreatStackRequestError(e),
                    exc_info[2]
                )

        if not resp.ok:
            if 'application/json' in resp.headers.get('Content-Type'):
                raise ThreatStackAPIError(
                    resp.reason,
                    resp.status_code,
                    resp.json()
                )
            else:
                raise ThreatStackRequestError(resp.reason, resp.status_code)

        return resp.json()

