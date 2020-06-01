#!/usr/bin/env python

# this lambda function will take apigateway event and respond with a message
# query apigateway endpoints and give list of api keys avaialable in account.

__author__ = 'aalam'

import logging
import json
import traceback
import gzip
import boto3
import base64

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def response(msg, statuscode, header={}, ):
    """

    :param msg: response message
    :param header: response header if any
    :param statuscode: status code of lambda execution

    :return:  return response to lambda invoking client( in this case api gateway)
    """
    if statuscode == 200:
        pass
    else:
        logger.error(msg)
    return {"body": msg, "headers": header, "statusCode": statuscode,
            "isBase64Encoded": False}


def handler(event, context):
    """
    Handler for load event from cloudwatch request
    :param event: cloudwatch log
    :param context: context of event

    """
    # print(f'Logging Event: {event}')
    # print(f"Awslog: {event['awslogs']}")
    cw_data = event['awslogs']['data']
    # print(f'data: {cw_data}')
    # print(f'type: {type(cw_data)}')
    compressed_payload = base64.b64decode(cw_data)
    uncompressed_payload = gzip.decompress(compressed_payload)
    payload = json.loads(uncompressed_payload)

    client = boto3.client('dynamodb')

    log_events = payload['logEvents']
    for log_event in log_events:
        print(f'LogEvent: {log_event["message"]}')

        message = json.loads(log_event["message"])
        requestId = message['requestId']
        requestTime = message['requestTimeEpoch']
        httpMethod = message['httpMethod']
        resourcePath = message['resourcePath']
        apikeyId = message['apikeyId']
        stage = message['stage']
        status = message['status']

        client.put_item(
            TableName='api_call_logs',
            Item={
                'requestId': {'S': requestId},
                'requestTime': {'S': requestTime},
                'httpMethod': {'S': httpMethod},
                'resourcePath': {'S': resourcePath},
                'apikeyId': {'S': apikeyId},
                'stage': {'S': stage},
                'status': {'S': status},
            }
        )


if __name__ == "__main__":
    # dummy event to test locally
    event = {
  "awslogs": {
    "data": "H4sIAAAAAAAAAIVRTY/aMBD9K8jHlg/bib9yQyqllYq0EtlTs1oFexaihti1HdoV4r/XJGzFqofaB8tv5r15M3NGRwih3kP56gAV6NOyXD5vVtvtcr1CU2R/deATjJUignOOmcQJbu1+7W3vUqTWOgkkYIS30UN9vDIAeG1yLFi+M1oTI2mWqRetMwNKK5HSQ78L2jcuNrb73LQRfEDFd+Q8mEbHZw8/ewgRPQ3CqxN08Ro/o8Yk/YzlBEuZ5znmmHJCmRCK5YxKLAWThKhcKqEooYLxBHDKFVMZT3Vjk3qO9THZJ0yKdJVgTObTt1kk+fOkQjcDX02FigrpTNRGCTozBF5mec1gppShM7qDHQdtuJS0QtPEa1wipFdkcyXmhNA5kXgM6bptwQ96sxHpw93/b80yWRxQyhdL5xcUU1xgVlBVZGzyEacz0u/yV87qw0B619Uge4jRbSAe7NjLelXeqgXbew0PdRyZC+etWdw2MFZIk4p9GM0MVau0IRuttu0AfinLhwWZkzc/wdkuwDfo9jfN/B/S5B2rQrVrfsDrkPzhv6fpHteb4x3vtp8TP5n2N0k9D7Fkez+O8NpShS7o8nT5A9ehA2buAgAA"
  }
}
    context = {"function_name": "first_lambda_function"}
    handler(event, context)
