from datetime import datetime, timedelta
from hashlib import sha256
import random
from socket import gethostbyname, gaierror


def dyre_dga(num, date_str=None):
    if date_str is None:
        date = datetime.now()
        date_str = date.strftime("%y-%m-%d")
    tlds = ['.cc', '.ws', '.to', '.in', '.hk', '.cn', '.tk', '.so']
    kk = '{0}{1}'.format(date_str, num)
    hash = sha256(kk.encode()).hexdigest()[3:36]

    replace_char = chr(0xFF & ((num % 26) + 97))

    hostname = '{0}{1}{2}'.format(replace_char, hash, tlds[num % len(tlds)])
    return hostname


def get_domains(nr=10000):
    num_days = int(nr) # generate 100 domains every daye
    domain_list=[]
    for d in range(num_days):
        num = random.randint(1, nr)
        date = datetime.now() - timedelta(days=num_days)
        date_str = date.strftime("%Y-%M-%d")
        domain_list= [*domain_list, dyre_dga(num,date_str)]
    return domain_list

if __name__=='__main__':
    print(len(get_domains()))