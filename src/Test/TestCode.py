import json
import requests
import time
import argparse
from random import randint
from pprint import pprint




def parse_arg():
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('--baseurl','-e', help='Description for baseurl argument', required=True)
    parser.add_argument('--predictkey', '-p', help='Description for predict endpoint key argument', required=True)
    parser.add_argument('--billingkey', '-b', help='Description for billing endpoint key argument', required=True)
    parser.add_argument('--testkey', '-t', help='Description for predict endpoint key argument', required=True)
    args = vars(parser.parse_args())
    return args


if __name__ == '__main__':
    args = parse_arg()

    TESTING = args['testkey']
    USER1 = args['predictkey']
    USER2 = args['billingkey']
    BASE_ENDPOINT = args['baseurl']

    while True:
        HEADER = 'x-api-key'
        fqdn_endpoint = f'{BASE_ENDPOINT}/predict'
        fqdn_api_key = USER1
        fqdn = 'www.google.com'
        # Add a random number of calls to the predict API
        loops = randint(20,100)
        for cnt in range(loops):
            print('LOOP:', cnt)
            payload = {'fqdn': fqdn }
            headers = {HEADER: fqdn_api_key}
            response = requests.get(url=fqdn_endpoint, headers=headers, params=payload)
            if response.reason != 'OK':
                print('FAIL')
                pprint(json.loads(response.text))
            blob = json.loads(response.text)
            if blob['fqdn'] != fqdn:
                print('FAIL')
            time.sleep(1)

    # Test with no API Key
        fqdn_api_key = ''
        headers = {HEADER: fqdn_api_key}
        response = requests.get(url=fqdn_endpoint, headers=headers, params=payload)
        if response.reason == 'OK':
            print('FAIL')
            exit(0)
        print('Error Message:', response.text)

        api_keys_endpoint = f'{BASE_ENDPOINT}/apikeys'
        billing_endpoint = f'{BASE_ENDPOINT}/billing'
        billing_api_key = USER2

        # Get all the api keys,
        headers = {HEADER: billing_api_key}
        response = requests.get(url=api_keys_endpoint, headers=headers)
        if response.reason != 'OK':
            print('FAIL')

        # Turn the return in a python list
        api_keys = json.loads(response.text)

        # print all the API keys, and counts
        for api_key in api_keys:
            payload = {'api_key': api_key}
            response = requests.get(url=billing_endpoint, headers=headers, params=payload)
            if response.reason != 'OK':
                print('FAIL')
                pprint(response.text)
                exit(0)
            billing_info = json.loads(response.text)
            print(billing_info['api_key'], billing_info['count'])