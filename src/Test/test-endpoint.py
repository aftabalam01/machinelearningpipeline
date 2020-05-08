import json
import requests
import argparse
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
        with open('assignment.csv', mode='r', encoding='utf-8') as ih:
            line = ih.readline()
            while True:
                line = ih.readline().strip("\n")
                if line == '':
                    break
                tokens = line.split(',')
                #print(tokens)
                domain = tokens[0]
                threat = tokens[1]
                domain = domain.lstrip().rstrip().lower()
                threat = threat.lstrip().rstrip().lower()
                fqdn = domain
                payload = {'fqdn': fqdn }
                headers = {HEADER: fqdn_api_key}
                response = requests.get(url=fqdn_endpoint, headers=headers, params=payload)
                if response.reason != 'OK':
                    print('FAIL')
                    pprint(json.loads(response.text))
                blob = json.loads(response.text)
                if blob['fqdn'] != fqdn:
                    print('FAIL')
                if (blob['dga'] == True and threat == 'dga') or (blob['dga'] == False and threat == 'benign'):
                    right += 1.0
                else:
                    wrong += 1.0

        print('Right: ', right, ' Wrong: ', wrong, 'Score: ', (right / (right + wrong)) * 100.0)
