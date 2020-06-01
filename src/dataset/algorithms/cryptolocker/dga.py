from datetime import datetime , timedelta
tlds = ["com", "net", "biz", "ru", "org", "co.uk", "info"]


def cryptolocker(date):
    domains = []
    for z in range(1000):
        d = date.day
        m = date.month
        y = date.year + z

        d *= 65537
        m *= 65537
        y *= 65537

        s = d >> 3 ^ y >> 8 ^ y >> 11
        s &= 3
        s += 12

        n = ""
        for i in range(s):
            d = ((d << 13 & 0xFFFFFFFF) >> 19 & 0xFFFFFFFF) ^ ((d >> 1 & 0xFFFFFFFF) << 13 & 0xFFFFFFFF) ^ (
                        d >> 19 & 0xFFFFFFFF)
            d &= 0xFFFFFFFF
            m = ((m << 2 & 0xFFFFFFFF) >> 25 & 0xFFFFFFFF) ^ ((m >> 3 & 0xFFFFFFFF) << 7 & 0xFFFFFFFF) ^ (
                        m >> 25 & 0xFFFFFFFF)
            m &= 0xFFFFFFFF
            y = ((y << 3 & 0xFFFFFFFF) >> 11 & 0xFFFFFFFF) ^ ((y >> 4 & 0xFFFFFFFF) << 21 & 0xFFFFFFFF) ^ (
                        y >> 11 & 0xFFFFFFFF)
            y &= 0xFFFFFFFF

            n += chr(ord('a') + (y ^ m ^ d) % 25)

        domain = n + "." + tlds[z % 7]
        domains.append(domain)
    return domains # only return unique


def get_domains(nr=10000):
    domains=[]
    for i in range(int(nr/1000)):
        date= datetime.now() - timedelta(days=i)
        domains +=cryptolocker(date)
    return domains

if __name__ == '__main__':

    for i in range(1,10):
        date = datetime.now() - timedelta(days=i)
        print(cryptolocker(date))
