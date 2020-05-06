#!/usr/bin/env python

# serverless database query - mysql RDS
# this lambda function will take apigateway event and respond with a message

__author__ = 'aalam'


import logging
import json
import traceback
import boto3
import requests
import calendar
from requests_aws_sign import AWSV4Sign
from datetime import datetime, timedelta

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
        print(msg)
    else:
        logger.error(msg)
    return {"body": msg,  "headers": header,  "statusCode": statuscode,
            "isBase64Encoded": False}


operations = ['GET', 'POST', 'PUT']


def handler_using_usage_api(event, context):
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

            api_id = payload.get('api_key', None)
            startDate = payload.get('startDate', (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
            endDate = payload.get('endDate', (datetime.now()).strftime("%Y-%m-%d"))
            session = boto3.session.Session()
            credentials = session.get_credentials()

            # You must provide an AWS region
            region = session.region_name or 'us-west-2'
            service = 'apigateway'

            auth = AWSV4Sign(credentials, region, service)
            endpoint = f'https://{service}.{region}.amazonaws.com/usageplans'
            payload= {"keyId":api_id}

            res = requests.get(endpoint, auth=auth, params=payload)
            usage_ids = res.json()['_embedded']['item']
            usage_id = usage_ids['id']
            usage_name=usage_ids['name']

            usage_details = requests.get(f"https://apigateway.us-west-2.amazonaws.com//usageplans/{usage_id}/usage?startDate={startDate}&endDate={endDate}",
                                             auth=auth)
            usage_count = 0
            try:
                values = usage_details.json().get('values',0).get(api_id,0)
                for value in values:
                    usage_count = usage_count + value[0]
            except:
                print("Error while getting values")
            bill_inf0 = {"api_key":api_id,"count": usage_count,"usage_plan":usage_name,"usage_id":usage_id,"startDate":startDate,"endDate":endDate}
            return response(msg=f"{bill_inf0}".replace("\'", "\""), statuscode=200)
        except Exception as e:
            response(msg=f"An exepection occurred {traceback.format_exc()}", statuscode=500)
    else:
        return response(msg=f"Input message is null\n.", statuscode=200)


def handler_using_db(event, context):
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

            api_id = payload.get('api_key', None)

            startDate = payload.get('startDate', None)
            endDate = payload.get('endDate', None)
            if startDate:
                startDate = datetime.strptime(startDate,'%Y-%m-%d')
            else:
                startDate = datetime.now() - timedelta(days=30)
            if endDate:
                endDate = datetime.strptime(endDate, '%Y-%m-%d')
            else:
                endDate = datetime.now()

            session = boto3.session.Session()
            credentials = session.get_credentials()

            # You must provide an AWS region
            region = session.region_name or 'us-west-2'
            service = 'apigateway'

            auth = AWSV4Sign(credentials, region, service)
            endpoint = f'https://{service}.{region}.amazonaws.com/usageplans'
            payload= {"keyId":api_id}

            res = requests.get(endpoint, auth=auth, params=payload)
            usage_ids = res.json()['_embedded']['item']
            usage_id = usage_ids['id']
            usage_name=usage_ids['name']

            start_epochtime= calendar.timegm(startDate.timetuple())
            end_epochtime = calendar.timegm(endDate.timetuple())

            print(f"{api_id}\t{start_epochtime}\t{end_epochtime}")
            success_code="200"

            client = boto3.client('dynamodb')
            res = client.scan(
                TableName='api_call_logs',
                FilterExpression="#A = :api_id AND #T < :end_epochtime AND #T > :start_epochtime AND #S = :status_code",
                ExpressionAttributeNames={
                    "#A": "apikeyId", "#T": "requestTime", "#S": "status"
                },
                ExpressionAttributeValues={
                    ":api_id": {"S": api_id},
                    ":start_epochtime": {"S": str(start_epochtime)},
                    ":end_epochtime": {"S": str(end_epochtime)},
                    ":status_code" : {"S": success_code}
                },
                Select='COUNT'
                )
            bill_inf0 = {"api_key": api_id, "count": res['Count'], "usage_plan": usage_name, "usage_id": usage_id,
                         "startDate": startDate.strftime("%Y-%m-%d"), "endDate": endDate.strftime("%Y-%m-%d")}

            return response(msg=f"{bill_inf0}".replace("\'", "\""), statuscode=200)

        except Exception as e:
            response(msg=f"An exception occurred {traceback.format_exc()}", statuscode=500)
    else:
        return response(msg=f"Input message is null\n.", statuscode=200)

if __name__ == "__main__":
    # dummy event to test locally
    event = {"httpMethod": "GET", "queryStringParameters":
                {"api_key": "shaq50ytsf","startDate":"2020-04-01","endDate":"2020-04-30"}}
    context = {"function_name": "first_lambda_function"}
    handler_using_db(event, context)
