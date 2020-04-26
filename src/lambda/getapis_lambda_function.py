#!/usr/bin/env python

# this lambda function will take apigateway event and respond with a message
# query apigateway endpoints and give list of api keys avaialable in account.

__author__ = 'aalam'

import logging
import json
import traceback
import boto3
import requests
from requests_aws_sign import AWSV4Sign

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
            payload =includevalues = None
            if operation in operations:
                payload = event.get('queryStringParameters',None) if operation == 'GET' else json.loads(event['body'])

            if payload:
                includevalues = payload.get('includeValues', False)
            if includevalues and includevalues.lower() == 'true':
                includevalues = True
            else:
                includevalues = False

            # get credential form role using boto3 libs
            session = boto3.session.Session()
            credentials = session.get_credentials()

            # You must provide an AWS region
            region = session.region_name or 'us-west-2'
            service = 'apigateway'

            auth = AWSV4Sign(credentials, region, service)
            endpoint = f'https://{service}.{region}.amazonaws.com/apikeys?includeValues={includevalues}'

            r = requests.get(endpoint, auth=auth)
            item_list = r.json()['_embedded']['item']
            key_list = []
            for item in item_list:
                if includevalues:
                    key_details = {"name": {item['name']}, "id": item['id'], "value": item.get('value', None),
                                   "descrpition": item['description']}
                else:
                    key_details = {"name": item['name'], "id": item['id'],
                                   "descrpition": item['description']}

                key_list = [*key_list, key_details]
                # usage_ids = requests.get(f"https://apigateway.us-west-2.amazonaws.com/usageplans?keyId={item['id']}", auth=auth)
                # usages = usage_ids.json()['_embedded']['item']
                # usage_details = requests.get(f"https://apigateway.us-west-2.amazonaws.com//usageplans/{usages['id']}/usage?startDate=2020-04-01&endDate=2020-04-30",
                #                              auth=auth)
            ret_response = {"key_list": key_list}
            return response(msg=f"{ret_response}".replace("\'", "\""), statuscode=r.status_code)

        except Exception as e:
            response(msg=f"An exepection occurred {traceback.format_exc()}", statuscode=500)

    else:
        return response(msg=f"Input message is null.\n", statuscode=200)


if __name__ == "__main__":
    # dummy event to test locally
    event = {"httpMethod": "GET", "queryStringParameters": {"includeValues": False}}
    context = {"function_name": "first_lambda_function"}
    handler(event, context)
