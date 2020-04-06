#!/usr/bin/env python

# serverless database query - mysql RDS
# this lambda function will take apigateway event and respond with a message

__author__ = 'harnan_group3'

import logging
import json
import traceback

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def response(msg, statuscode, header={},):
    """

    :param msg: response message
    :param header: response header if any
    :param statuscode: status code of lambda execution

    :return:  return response to lambda invoking client( in this case api gateway)
    """
    if statuscode == 200:
        logger.info(msg)
    else:
        logger.error(msg)
    return {"body": msg,  "headers": header,  "statusCode": statuscode,
            "isBase64Encoded": False}


operations = ['GET']


def handler(event, context):
    """
    Handler for APIGATEWAY request
    :param record: api gateway msg/event
    :param context: context of event

    :return: returns fqdn from api gateway requests
    """
    print(event)
    if event:
        try:
            operation = event['httpMethod']
            #eventsourcerarn = record['eventSourceARN']

            if operation in operations:
                payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
                fqdn = payload.get('fqdn', None)

            else:
                return response(msg=f"ERROR: Operation {operation} is not supported \n", statuscode=400)

        except Exception as e:
                return response(msg=f"ERROR: Cannot process records .{traceback.format_exc()}\n", statuscode=400)

        return response(msg=f"fqdn sent in message is {fqdn}\n", statuscode=200)

    else:
        return response(msg=f"Input message is null\n", statuscode=200)


if __name__ == "__main__":
    # dummy event to test locally
    event = {}
    context = {"function_name": "first_lambda_function"}
    handler(event, context)
