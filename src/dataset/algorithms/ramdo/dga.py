
class Ramdo:
    def __init__(self,count=20):
        self.domaincount=count
        self.domains=[]
        self.domaincount=count

    def dga(self, seed, nr):
        s = (2 * seed * (nr + 1))
        r = s ^ (26 * seed * nr)
        domain = ""
        for i in list(range(16)):
            r = r & 0xFFFFFFFF
            domain += chr(r % 26 + ord('a'))
            r += (r ^ (s*i**2*26))

        domain += ".org"
        return domain

    def generate_dga(self,count=None):
        if count:
            self.domaincount = count
        for nr in range(self.domaincount):
            self.domains=[*self.domains, self.dga(0xD5FFF, nr)]
        return self.domains


if __name__ == 'main':
    Ramdo().generate_dga()
