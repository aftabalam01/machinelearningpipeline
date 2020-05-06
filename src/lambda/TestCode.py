import json
import requests
import time
from random import randint
from pprint import pprint

TESTING = 'vpV9sLaviN3xCDMbq1Htd2PUhw75zJcP3dHunf78'
USER1 = 'SOJQO9h7Th83obI3MrR0s29PU8Pq01Fh3eCmJNXB'
USER2 = 'VS2fxU0EYG4wLUFyduL2noVdxoSNxZM4pzReIGa0'

BASE_ENDPOINT='https://2m8bl9b05i.execute-api.us-west-2.amazonaws.com/prod'

if __name__ == '__main__':

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