'''
Send alert events to datadog.
'''

from flask import Blueprint, jsonify, request
import logging
import app.models.datadog as datadog_model
import app.models.threatstack as threatstack_model

_logger = logging.getLogger(__name__)

datadog = Blueprint('datadog', __name__)

class DataDogToTSBaseError(Exception):
    status_code = 400

#decerator refers to the blueprint object.
@datadog.route('/status', methods=['GET'])
def is_available():
    '''
    Test that Threat Stack and datadog bucket are reachable.
    '''
    dd = datadog_model.DataDogModel()
    datadog_status = dd.is_available()
    datadog_info = {'success': datadog_status}

    ts = threatstack_model.ThreatStackModel()
    ts_status = ts.is_available()
    ts_info = {'success': ts_status}

    status_code = 200
    success = True

    return jsonify(success=success, datadog=datadog_info, threatstack=ts_info), status_code

@datadog.route('/alert', methods=['POST'])
def put_alert():
    '''
    Archive Threat Stack alerts to datadog.
    '''
    webhook_data = request.get_json()
    datadog_response_list = []
    for alert in webhook_data.get('alerts'):
        ts = threatstack_model.ThreatStackModel()
        alert_full = ts.get_alert_by_id(alert.get('id'))

        dd = datadog_model.DataDogModel()
        datadog_response = dd.put_alert_event(alert_full)
        datadog_response_list.append(datadog_response)

    status_code = 200
    success = True
    response = {'success': success, 'datadog': datadog_response_list}

    return jsonify(response), status_code

