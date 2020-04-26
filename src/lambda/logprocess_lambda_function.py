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
    event = {"httpMethod": "GET", "queryStringParameters": {"includeValues": False}}
    context = {"function_name": "first_lambda_function"}
    handler(event, context)
