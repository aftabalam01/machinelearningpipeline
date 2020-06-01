from datetime import datetime, timedelta
import  random

def rand(seed):
    seed = (seed * 0x41c64e6d + 0x3039) & 0xffffffff
    return seed, (seed >> 0xa)


def vidro(epoch, nr):
    tlds = ['org', 'com', 'net']
    seed_init = 0x1e240 * \
                (((epoch - 0x4BEFB280) << 32) / (0x93a80 << 32) + 0x3ed)
    domains = []
    for i in range(nr):
        seed = i % 100 + seed_init
        seed, r = rand(int(seed))
        sld_len = r % 6 + 7

        domain = ''
        for _ in range(sld_len):
            seed, r = rand(int(seed))
            domain += chr(r % 26 + ord('a'))

        domain += '.' + tlds[i % 3]
        domains = [*domains,domain]
    return domains


def get_domains(nr=10000):
    num_days = int(nr/100) # generate 100 domains every daye
    epoch_time=15500000
    domain_list=[]
    for d in range(num_days):
        hours = random.randint(9, 20)
        minutes = random.randint(0, 59)
        seconds = random.randint(0, 60)
        date = datetime.now() - timedelta(days=num_days,hours=hours,minutes=minutes,seconds=seconds)
        epoch_time = int(date.timestamp())
        domain_list += vidro(epoch_time, 100)
    return domain_list


if __name__=='__main__':
    print(get_domains())