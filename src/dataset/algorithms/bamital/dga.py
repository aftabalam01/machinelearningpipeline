import hashlib
import datetime
from datetime import datetime, timedelta
import random


tlds = [".org"]


def bamital(date):
    first_letter = random.randint(65, 74)
    last_letter = random.randint(75, 90)
    letter = first_letter
    doms = []
    while (letter <= last_letter):

        dom = hashlib.md5((chr(letter) + date).encode()).hexdigest()

        domain = dom + (random.choices(tlds, k=1)[0])

        letter += 1
        doms = [*doms,domain]

    return doms

def get_domains(count=10000):
    domains=[]
    for i in range(int(count/60)):
        date = datetime.now() - timedelta(days=i)
        domains += bamital(date.strftime("%Y-%m-%d"))
    return domains

if __name__=='__main__':
    print(get_domains(1000))