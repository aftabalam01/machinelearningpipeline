from datetime import datetime
from ctypes import c_uint
import argparse
import os

wordlists = {'luther': (4, '.com'), 'rfc4343': (3, '.com'), 'nasa': (5, '.com')}

seeds = {
        'luther': {'div': 4, 'tld': '.com', 'nr': 12},
        'rfc4343': {'div': 3, 'tld': '.com', 'nr': 10},
        'nasa': {'div': 5, 'tld': '.com', 'nr': 12},
        'gpl': {'div': 5, 'tld': '.ru', 'nr': 10}
        }
        
        
class Rand:

    def __init__(self, seed):
        self.r = c_uint(seed) 

    def rand(self):
        self.r.value = 1664525*self.r.value + 1013904223
        return self.r.value


def get_words(wordlist):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path+"/"+wordlist, 'r') as r:
        return [w.strip() for w in r if w.strip()]

class Gozi:
    def __init__(self,word =None,date=None,count=None):
        if not word:
            self.wordlist=seeds.keys()
        else:
           self.wordlist =[word]
        self.date= datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
        self.domains=[]
        self.domaincount = count if count else 100

    def dga(self, wordlist,date=None):
        words = get_words(wordlist)
        if not date:
            date = self.date
        diff = date - datetime.strptime("2015-01-01", "%Y-%m-%d")
        days_passed = (diff.days // seeds[wordlist]['div'])
        flag = 1
        seed = (flag << 16) + days_passed - 306607824
        r = Rand(seed)
        c = len(self.wordlist)
        for i in range(round(self.domaincount/c)):
            r.rand()
            v = r.rand()
            length = v % 12 + 12
            domain = ""
            while len(domain) < length:
                v = r.rand() % len(words)
                word = words[v]
                l = len(word)
                if not r.rand() % 3:
                    l >>= 1
                if len(domain) + l <= 24:
                    domain += word[:l]
            domain += seeds[wordlist]['tld']
            self.domains = [*self.domains,domain]
        return self.domains

    def generate_domain(self):
        for word in self.wordlist:
            self.dga(word)
        return self.domains


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="gozi dga")
#     parser.add_argument("-d", "--date",
#             help="date for which to generate domains")
#     parser.add_argument("-w", "--wordlist", help="wordlist",
#             choices=seeds.keys(), default='luther')
#     args = parser.parse_args()
#     if args.date:
#         d = datetime.strptime(args.date, "%Y-%m-%d")
#     else:
#         d = datetime.now()
#
#     g = Gozi(word=args.wordlist, date=d)
#     print(g.generate_domain())
