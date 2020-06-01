#!/usr/bin/env python

# serverless database query - mysql RDS
# this lambda function will take apigateway event and respond with a message

__author__ = 'aalam'

import os
import logging
import json
import traceback
import tldextract
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# grab environment variables
ENDPOINT_NAME = os.getenv('ENDPOINT_NAME', 'XGBoostEndpoint-2020-05-08-14-42-46')
VALID_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789-_.'
LOOKUP_TABLE = None


def extract_domain(record):
    domain = record
    ret = ''
    try:
        ext = tldextract.extract(domain)
        ret = ext.domain
    except:
        print(record)
    return ret


def pad(l, content, width):
    l.extend([content] * (width - len(l)))
    return l


def features(domain):
    global VALID_CHARS
    global LOOKUP_TABLE
    if not LOOKUP_TABLE:
        LOOKUP_TABLE = dict()
        idx = 1
        for c in VALID_CHARS:
            LOOKUP_TABLE[c] = int(idx)
            idx += int(1)
    rvalue = list()
    if len(domain) <= 63 and ' ' not in domain:
        for c in domain.lower():
            rvalue.append(str(LOOKUP_TABLE[c]))
    else:
        # print(domain)
        pass
    rvalue = pad(rvalue, '0', 63)
    return ','.join(rvalue)


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
                runtime = boto3.client('runtime.sagemaker')
                domain = extract_domain(fqdn)
                feature_X = features(domain)
                # print(feature_X)
                res = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                              ContentType='text/csv',
                                              Body=feature_X)
                # print(response)
                pred = json.loads(res['Body'].read().decode())
                print(pred)
                is_dga = True if pred > .5 else False
                # call predict endpoint here
                res_payload = {'fqdn': fqdn, 'dga': is_dga}
                logger.info(msg=res_payload)
                # print(payload)
                return response(msg=f"{json.dumps(res_payload)}", statuscode=200)

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
