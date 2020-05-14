from datetime import datetime
import hashlib
import argparse

tlds = [
    ".org",
    ".tickets",
    ".blackfriday",
    ".hosting",
    ".feedback",
]

magic = "jkhhksugrhtijys78g46"
special = "31b4bd31fg1x2"


def generate_domains(date, back=0,nr=500):

    ndays = (date - datetime(1970, 1, 1)).days
    # days_since_epoch
    domains=[]
    for j in range(back+1):
        for nr in range(nr):
            for tld in tlds:
                seed = "{}-{}-{}".format(magic, ndays, nr)
                m = hashlib.md5(seed.encode('ascii')).hexdigest()
                mc = m[:13]
                if nr == 0:
                    sld = special
                else:
                    sld = mc

                domain = "{}{}".format(sld, tld)
                #yield domain
                domains = [*domains,domain]
        ndays -= 1
        return domains


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-d", "--date", help="date when domains are generated")
#     args = parser.parse_args()
#     if args.date:
#         d = datetime.strptime(args.date, "%Y-%m-%d")
#     else:
#         d = datetime.now()
#     for domain in generate_domains(d):
#         print(domain)
