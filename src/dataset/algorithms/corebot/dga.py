import argparse
from datetime import datetime

class Corebot:
    def __init__(self,seed="1DBA8930",date=datetime.now(),debug=False,count=40):
        """

        """
        self.seed = seed
        self.date = date
        self.day= 8 if debug else date.day
        self.domaincount=count
        self.domains=[]

    def init_rand_and_chars(self,year, month, day, nr_b, r):
        r = (r + year + ((nr_b << 16) + (month << 8) | day)) & 0xFFFFFFFF
        charset = [chr(x) for x in range(ord('a'), ord('z'))] +\
                [chr(x) for x in range(ord('0'), ord('9'))]

        return charset, r

    def _generate_domain(self, charset, r):
        len_l = 0xC
        len_u = 0x18
        r = (1664525 * r + 1013904223) & 0xFFFFFFFF
        domain_len = len_l + r % (len_u - len_l)
        domain = ""
        for i in range(domain_len, 0, -1):
            r = ((1664525 * r) + 1013904223) & 0xFFFFFFFF
            domain += charset[r % len(charset)]
        domain += ".net"
        self.domains = [*self.domains, domain]
        return r

    def generate_domain(self):

        charset, r = self.init_rand_and_chars(self.date.year, self.date.month, self.date.day, 1, int(self.seed, 16))
        for _ in range(self.domaincount):
            r = self._generate_domain(charset, r)
        return list(set(self.domains))


# if __name__=="__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-s", "--seed", help="seed", default="1DBA8930")
#     parser.add_argument("-d", "--date", help="date for which to generate domains")
#     parser.add_argument("-t", "--debug", help="debug DGA (day set to 8)")
#     parser.add_argument("-n", "--nr", help="nr of domains to generate",
#            type=int, default=40)
#     args = parser.parse_args()
#
#     d = datetime.strptime(args.date, "%Y-%m-%d") if args.date else datetime.now()
#     day = 8 if args.debug else d.day
#     cb =Corebot(seed=args.seed, date=d,debug=False,count=args.nr)
#     cb.generate_domain()

    
    
