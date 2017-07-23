'''
Communicate with Threat Stack
'''
from app.errors import AppBaseError
import config
import logging
import requests
import six
import sys
import threatstack

_logger = logging.getLogger(__name__)

THREATSTACK_API_KEY = config.THREATSTACK_API_KEY
THREATSTACK_BASE_URL = config.THREATSTACK_BASE_URL

class ThreatStackBaseError(AppBaseError):
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
        self._threatstack_client = threatstack.ThreatStack(THREATSTACK_API_KEY)

    def is_available(self):
        '''
        Check connectivity to Threat Stack.

        Returns a failure if cannot connect to Threat Stack API.  This could be
        anything from API credential issues to connection failure.
        '''

        available = False
        try:
            for org in self._threatstack_client.organizations.list():
                if org:
                    available = True
                    break
        except threatstack.ThreatStackAPIError as e:
            raise ThreatStackAPIError(e.message)
        # Module doesn't handle the None response that occurs on bad API key.
        except TypeError:
            pass

        return available

    def get_agent_by_id(self, agent_id):
        '''
        Get agent info for the given ID
        '''
        try:
            resp = self._threatstack_client.agents.get(agent_id)
        except threatstack.ThreatStackAPIError as e:
            raise ThreatStackAPIError(e)

        return resp

    def get_alert_by_id(self, alert_id):
        '''
        Retrieve an alert from Threat Stack by alert ID.
        '''
        try:
            resp = self._threatstack_client.alerts.get(alert_id)

        except threatstack.ThreatStackAPIError as e:
            raise ThreatStackAPIError(e)

        return resp
