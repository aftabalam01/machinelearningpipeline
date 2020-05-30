import json
import requests
import argparse
from time import sleep
from pprint import pprint


def parse_arg():
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('--baseurl','--endpoint', help='Description for baseurl argument', required=True)
    parser.add_argument('--apikey', '--k', help='Description for apikey argument', required=True)
    args = vars(parser.parse_args())
    return args


if __name__ == '__main__':

        args = parse_arg()

        HEADER = 'x-api-key'
        fqdn_endpoint = args['baseurl'] + '/predict'
        fqdn_api_key = args['apikey']
        right = float(0)
        wrong = float(0)
        with open('feedback.csv', mode='r', encoding='utf-8') as ih:
            line = ih.readline()
            while True:
                line = ih.readline()
                if line == '':
                    break
                tokens = line.split(',')
                domain = tokens[0]
                threat = tokens[1]
                domain = domain.lstrip().rstrip().lower()
                threat = threat.lstrip().rstrip().lower()
                fqdn = domain
                payload = {'fqdn': fqdn}
                headers = {HEADER: fqdn_api_key}
                response = None
                retry_delay = 1
                for retry in range(5):
                    bad_response = True
                    response = requests.get(url=fqdn_endpoint, headers=headers, params=payload)
                    if response.reason != 'OK':
                        print('FAIL')
                        print('HEADERS')
                        pprint(headers)
                        print('PAYLOAD')
                        pprint(payload)
                        print('RESPONSE')
                        pprint(response.text)
                        sleep(retry_delay)
                        retry_delay = 2 * retry_delay
                    else:
                        break
                    if bad_response == True and retry == 4:
                        print('Retries Exhausted Exiting')
                        exit(0)
                blob = json.loads(response.text)
                pthreat = 'benign'
                if 'dga' not in blob:
                    print('FAIL')
                    exit(0)
                if blob['dga'] == True:
                    pthreat = 'dga'
                if blob['fqdn'] != fqdn:
                    print('FAIL')
                    exit(0)
                if (blob['dga'] == True and threat == 'dga') or (blob['dga'] == False and threat == 'benign'):
                    right += 1.0
                    #print('Pass,' + fqdn + ',' + threat + ',' + pthreat)
                else:
                    wrong += 1.0
                    print('Fail,' + fqdn + ',' + threat + ',' + pthreat)

        print('Right: ', right, ' Wrong: ', wrong, 'Score: ', (right / (right + wrong)) * 100.0)
