from datetime import datetime , timedelta
import time
import random

def tofsee(r):
    domain = ""
    while True:
        domain += chr(r % 26 + ord('a'))
        r //= 26
        if not r:
            break
    for i in range(27):
        for tld in ['.biz']:
            yield 2 * domain[::-1] + chr(i%26 + ord('a')) + tld


def get_domain(date):
    unixtimestamp = int(date.timestamp())
    seed = int(unixtimestamp)
    domains = []
    for domain in tofsee(seed):
        domains = [*domains,domain]
    return domains

def get_domains(count=1000):
    domains = []
    for i in range(int(count/26)):
        hours = random.randint(9, 20)
        minutes = random.randint(0, 59)
        seconds = random.randint(0, 60)
        date = datetime.now() - timedelta(days=i, hours=hours, minutes=minutes, seconds=seconds)
        domains += get_domain(date)
    return domains

if __name__ == '__main__':

    for i in range(1,10):
        date = datetime.now() - timedelta(days=i)
        print(get_domains(date))

