'''
    DGA of CCleaner
'''


from datetime import datetime, timedelta


def msvcrt_rand(seed):
    new_seed = (0x343fd * seed + 0x269ec3) & ((1 << 32) - 1)
    randval = (new_seed >> 16) & 0x7fff
    return randval, new_seed


def get_domains(nr, tlds=[".com"]):
    domains = []
    for i in range(nr):

        date = datetime.now() - timedelta(days=i)
        r1, seed = msvcrt_rand(date.year * nr + date.month+date.day)
        r2, seed = msvcrt_rand(seed)
        r3, seed = msvcrt_rand(seed)

        sld = 'ab%x%x' % (r2 * r3, r1)

        domain = sld + '.' + tlds[0]
        domains = [*domains,domain]
    return domains

