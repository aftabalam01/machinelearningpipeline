import random
import hashlib
#import nltk
#nltk.download()
from nltk.corpus import words
tlds = ["com", "net", "biz", "ru", "org", "co.uk", "info"]
word_list = words.words()

def twoDigitHex( number ):
    return '%02x' % number


def enviserv(i):
    seed_str = random.choices(word_list, k=1)[0] + str(i)
    s = hashlib.sha1(seed_str.encode())
    x = s.hexdigest()
    domain = ""
    k = random.randint(150, 255)
    for j in range(k,k+random.randint(5, 10)):
        domain += twoDigitHex(j)

    domain += '.' + tlds[i % 6]

    return domain


def get_domains(count=1000):
    domains= []
    for i in range(0,len(word_list)):
        domains = [*domains,enviserv(i)]
    return list(set(domains))


if __name__=='__main__':
    print(get_domains())