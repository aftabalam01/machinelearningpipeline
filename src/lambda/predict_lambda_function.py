#!/usr/bin/env python

# serverless database query - mysql RDS
# this lambda function will take apigateway event and respond with a message

__author__ = 'aalam'

import random
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


operations = ['GET', 'POST', 'PUT']


def handler(event, context):
    """
    Handler for APIGATEWAY request
    :param event: api gateway msg/event
    :param context: context of event

    :return: returns fqdn from api gateway requests
    """
    if event:
        try:
            operation = event['httpMethod']
            if operation in operations:
                payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
                fqdn = payload.get('fqdn', None)
                # call predict endpoint here
                logger.info(msg=payload)
                if random.randint(0, 10) % 2 == 0:
                    payload['dga'] = True
                else:
                    payload['dga'] = False
                logger.info(msg=payload)
                #print(payload)
                return response(msg=f"{json.dumps(payload)}", statuscode=200)

            else:
                return response(msg=f"ERROR: Operation {operation} is not supported \n.", statuscode=400)

        except Exception as e:
                return response(msg=f"ERROR: Cannot process records .{traceback.format_exc()}\n.", statuscode=400)
    else:
        return response(msg=f"Input message is null.\n", statuscode=200)


if __name__ == "__main__":
    # dummy event to test locally
    event = {"httpMethod": "GET", "queryStringParameters": {"fqdn": "google.com"}}
    context = {"function_name": "first_lambda_function"}
    handler(event, context)
