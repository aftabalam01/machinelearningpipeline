import argparse
from ctypes import c_int

class Rand:

    def __init__(self):
        self.r = c_int()

    def srand(self, seed):
        self.r.value = seed

    def rand(self):
        self.r.value = 214013*self.r.value + 2531011
        return (self.r.value >> 16) & 0x7FFF

    def randint(self, lower, upper):
        return lower + self.rand() % (upper - lower + 1)


class DnsChanger:
    def __init__(self,seed,count=100):
        r = Rand()
        r.srand(seed)
        self.r = r
        self.domains=[]
        self.domaincount=count

    def dga(self, r):
        sld = ''.join([chr(r.randint(ord('a'), ord('z'))) for _ in range(10)])
        return sld + '.com'

    def generate_domain(self):
        for _ in range(self.domaincount):
            self.domains = [*self.domains,self.dga(self.r)]
        return list(set(self.domains))


# if __name__=="__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("seed", type=int)
#     args = parser.parse_args()
#     r = Rand()
#     r.srand(args.seed)
#
#     d = DnsChanger(seed=args.seed,count=5)
#     d.generate_domain()
#     print(d.domains)
