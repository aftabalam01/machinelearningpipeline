import argparse

class RandInt:

    def __init__(self, seed): 
        self.seed = seed

    def rand_int_modulus(self, modulus):
        ix = self.seed
        ix = 16807*(ix % 127773) - 2836*(ix % 127773) & 0xFFFFFFFF
        self.seed = ix
        return ix % modulus 

class Dircypt:

    def __init__(self,seed=None,count=30):
        self.domaincount = count
        self.seed = int(seed,16)
        self.domains=[]

    def get_domains(self,seed, nr):
        r = RandInt(seed)
        for i in range(nr):
            domain_len = r.rand_int_modulus(12+1) + 8
            domain = ""
            for i in range(domain_len):
                char = chr(ord('a') + r.rand_int_modulus(25+1))
                domain += char
            domain += ".com"
            yield domain

    def generate_domain(self):
        for domain in self.get_domains(self.seed, self.domaincount):
            self.domains = [*self.domains,domain]
        return self.domains


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="generate Dircrypt domains")
    parser.add_argument("seed", help="seed as hex")
    args = parser.parse_args()
    domains= Dircypt().generate_domain()
    print(domains)