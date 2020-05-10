import argparse


class Fobber:
    def __init__(self,version=2,count=500):
        self.domaincount=count
        self.domains=[]
        self.version=version

    def ror32(self,v, n):
        return ((v >> n) | (v << (32 - n))) & 0xFFFFFFFF

    def next_domain(self,r, c, l, tld):
        domain = ""
        for _ in range(l):
            r = self.ror32((321167 * r + c) & 0xFFFFFFFF, 16);
            domain += chr((r & 0x17FF) % 26 + ord('a'))

        domain += tld
        self.domains = [*self.domains, domain]
        return r

    def dga(self):
        if self.version == 1:
            r = 0xC87C8A78
            c = -1719405398
            l = 17
            tld = '.net'
        elif self.version == 2:
            r = 0x851A3E59
            c = -1916503263
            l = 10
            tld = '.com'
        else: # default
            r = 0x851A3E59
            c = -1916503263
            l = 10
            tld = '.com'

        for _ in range(self.domaincount):
            r = self.next_domain(r, c, l, tld)



if __name__=="__main__":
    parser = argparse.ArgumentParser(description="DGA of Fobber")
    parser.add_argument("version", choices=[1,2], type=int)
    args = parser.parse_args()
    f= Fobber(version=args.version)
    f.dga()
    print(f.domains)



