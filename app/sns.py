'''
Handle SNS compatibility.
'''
from app.errors import AppBaseError
import boto3
from flask import jsonify, request
from functools import wraps
import json
import logging

_logger = logging.getLogger(__name__)

class SNSBaseError(AppBaseError):
    '''
    Base SNS error class
    '''
    status_code = 400

class SNSMessageInvalidError(SNSBaseError):
    '''
    SNS Message is invalid.
    '''

def _get_webhook_data(request_data):
    '''
    Handle Threat Stack vs. AWS SNS messages.
    '''
    webhook_data = None
    if 'TopicArn' in request_data.keys() and 'Message' in request_data.keys():
        if type(request_data['Message']) == dict:
            webhook_data = request_data.get('Message')
    else:
        webhook_data = request_data

    return webhook_data

def confirm_aws_sns_subscription(confirmation):
    '''
    Confirm an SNS subscription
    '''
    sns_client = boto3.client('sns')
    kwargs = {'TopicArn': confirmation['TopicArn'],
              'Token': confirmation['Token'],
              'AuthenticateOnUnsubscribe': 'true'}
    # If we fail an error is thrown.  Not going to return anything.  No need
    # since we should just be talking to another system that won't care what
    # we say.
    resp = sns_client.confirm_subscription(**kwargs)

    return resp

def check_aws_sns(func):
    '''
    Differentiates AWS SNS message vs. Threat Stack web hook.
    '''
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'X-Amz-Sns-Message-Type' in request.headers:
            if request.headers['X-Amz-Sns-Message-Type'] == 'SubscriptionConfirmation':
                # AWS doesn't set the content type to JSON on
                # SubScriptionConfirmation.
                request_data = request.get_json(force=True)
                confirm_aws_sns_subscription(request_data)
                return jsonify({}), 200
            else:
                request_data = request.get_json(force=True)
                try:
                    webhook_data = request_data.get('Message')  # This is a string os JSON inside the JSON doc.
                except json.JSONDecoderError:
                    _logger.info('SNS Message: {}'.format(request_data))
                    msg = 'Invalid request: {}'.format(request_data)
                    raise SNSMessageInvalidError(msg)

                # You can bypass _cached_json with get_json() but that relies
                # on get_data() which allows you to disable caching results
                # but not from using _cached_data if it exists.
                #
                # We'd have to manipulate the stream if we did a straight
                # delattr() here.
                setattr(request, '_cached_data', webhook_data)

                # This way we don't have to worry about how we call get_json()
                # after this.
                if '_cached_json' in dir(request):
                    delattr(request, '_cached_json')

        return func(*args, **kwargs)
    return decorated_function

