from datetime import datetime, timedelta
import base64 
import argparse 
import random


def dga(d, day_index, tld_index):
    tlds = [".com", ".org", ".net", ".info"]
    d -= timedelta(days=day_index)
    ds = d.strftime("%d%m%Y")
    return base64.b64encode(str.encode(ds)).lower().replace("=".encode(),"a".encode()) + str.encode(tlds[tld_index])


def generate_domains(date,count):
    domains=[]
    for i in range(count):
        domains = [*domains,dga(date, i%10, random.choice(range(4))).decode()]
    return domains


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date for which to generate domains")
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()

    print(generate_domains(d, count=40))

