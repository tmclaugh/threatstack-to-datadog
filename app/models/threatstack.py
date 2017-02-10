'''
Communicate with Threat Stack
'''
from app.errors import AppBaseError
import config
import logging
import requests
import six
import sys

_logger = logging.getLogger(__name__)

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

    def _make_threatstack_request(self, api_type, api_type_id=None, api_args=[]):
        '''
        Make a request to Threat Stack and get back a response.
        '''
        url_type = api_type
        if api_type_id:
            url_type_id = api_type_id
        else:
            url_type_id = ''

        if api_args:
            url_args = '?{}'.format('&'.join(api_args))
        else:
            url_args = ''

        alerts_url = '{}{}'.format(
            '/'.join([THREATSTACK_BASE_URL, url_type, url_type_id,]),
            url_args
        )

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

    def is_available(self):
        '''
        Check connectivity to Threat Stack.

        Returns a failure if cannot connect to Threat Stack API.  This could be
        anything from API credential issues to connection failure.
        '''

        if self._make_threatstack_request('alerts', api_args=['count=1']):
            available = True
        else:
            available = False

        return available

    def get_agent_by_id(self, agent_id):
        '''
        Get agent info for the given ID
        '''
        return self._make_threatstack_request('agents', agent_id,)

    def get_alert_by_id(self, alert_id):
        '''
        Retrieve an alert from Threat Stack by alert ID.
        '''
        return self._make_threatstack_request('alerts', alert_id,)

