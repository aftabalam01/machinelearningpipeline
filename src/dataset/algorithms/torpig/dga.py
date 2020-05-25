from datetime import datetime , timedelta
import random

suffixes = ["anj", "ebf", "arm", "pra", "aym", "unj", "ulj", "uag", "esp", "kot", "onv", "edc"]
tlds = ['.com', '.net', '.biz']


def torpig(date):
    if date.year < 2007:
      year = 2007
    else:
        year = date.year
    s = (((date.month ^ date.day) + date.day) * 8) + date.day + year
    c1 = (((date.year >> 2) & 0x3fc0) + s) % 25 + ord('a')
    c2 = (date.month + s) % 10 + ord('a')
    c3 = ((year & 0xff) + s) % 25 + ord('a')
    if date.day * 2 < ord('0') or date.day * 2 < ord('9'):
      c4 = (date.day * 2) % 25 + ord('a')
    else:
      c4 = date.day % 10 + ord('1')
    domain = chr(c1) + 'h' + chr(c2) + chr(c3) + 'x' + chr(c4) + suffixes[date.month - 1] + tlds[random.randint(0,2)]
    return domain


def get_domains(nr=10000):
    domains=[]
    for i in range(nr):
        date= datetime.now() - timedelta(days=i)
        domains = [*domains,torpig(date)]
    return list(set(domains))


if __name__=='__main__':
    print(get_domains())