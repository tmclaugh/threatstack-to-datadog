import os
import logging

THREATSTACK_API_KEY = os.environ.get('THREATSTACK_API_KEY')
THREATSTACK_BASE_URL = os.environ.get('THREATSTACK_BASE_URL', 'https://app.threatstack.com/api/v1')

DATADOG_API_KEY = os.environ.get('DATADOG_API_KEY')
DATADOG_APP_KEY = os.environ.get('DATADOG_APP_KEY')

LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
LOG_LEVEL = logging.INFO

