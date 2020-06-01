import argparse

class RandInt:

    def __init__(self, seed): 
        self.value = seed

    def rand_int_modulus(self, modulus):
        ix = self.value
        ix = 16807*(ix % 127773) - 2836*(ix // 127773) & 0xFFFFFFFF
        self.value = ix 
        return ix % modulus 

def get_domains(seed, nr, tlds=None):
    if not tlds:
        tlds = [".com"]

    r = RandInt(seed)
    domains=[]
    for i in range(nr):
        seed_a = r.value
        domain_len = r.rand_int_modulus(12) + 8
        seed_b = r.value
        domain = ""
        for j in range(domain_len):
            char = chr(ord('a') + r.rand_int_modulus(25))
            domain += char
        tld = tlds[i % len(tlds)]
        domain += '.' if tld[0] != '.' else ''
        domain += tld
        m = seed_a*seed_b
        r.value = (m + m//(2**32)) % 2**32 
        #yield domain
        domains =[*domains,domain]
    return domains


if __name__=="__main__":
    """ 
        example seeds:
            
    """
    parser = argparse.ArgumentParser(description="generate Ramnit domains")
    parser.add_argument("seed", help="seed as hex")
    parser.add_argument("nr", help="nr of domains", type=int)
    parser.add_argument("-t", "--tlds", help="list of tlds", default=None)
    args = parser.parse_args()
    tlds = None
    if args.tlds:
        tlds = [x.strip() for x in args.tlds.split(" ")]
    print(get_domains(int(args.seed, 16), args.nr, tlds))

