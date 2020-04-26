#!/usr/bin/env python

# serverless database query - mysql RDS
# this lambda function will take apigateway event and respond with a message

__author__ = 'aalam'


import logging
import json
import traceback
import boto3
import requests
from requests_aws_sign import AWSV4Sign



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
        session = boto3.session.Session()
        credentials = session.get_credentials()

        # You must provide an AWS region
        region = session.region_name or 'us-west-2'
        service = 'apigateway'

        auth = AWSV4Sign(credentials, region, service)
        endpoint = 'https://apigateway.us-west-2.amazonaws.com/apikeys'

        r = requests.get(endpoint, auth=auth)
        l =r.json()['_embedded']['item']
        for item in l:
            print(item['id'])
            usage_ids = requests.get(f"https://apigateway.us-west-2.amazonaws.com/usageplans?keyId={item['id']}", auth=auth)
            usages = usage_ids.json()['_embedded']['item']
            usage_details = requests.get(f"https://apigateway.us-west-2.amazonaws.com//usageplans/{usages['id']}/usage?startDate=2020-04-01&endDate=2020-04-30",
                                         auth=auth)
            print(usage_details.json())
        #return response(msg=f"keys are: {r.content}", statuscode=r.status_code)

    else:
        return response(msg=f"Input message is null\n.", statuscode=200)


if __name__ == "__main__":
    # dummy event to test locally
    event = {"afafa":1}
    context = {"function_name": "first_lambda_function"}
    handler(event, context)
