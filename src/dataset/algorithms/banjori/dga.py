
class Banjori:
    """

    """
    def __init__(self, count=1000):
        """

        :param count:
        """
        self.domaincount = count
        self.seed = ['happylifeisbetterlife.com','googlemodelmachine.com','mygardenisbetterthanyours.com'] # 15372 equal to 0 (seed = 0)

    def _map_to_lowercase_letter(self, s):
        return ord('a') + ((s - ord('a')) % 26)

    def _next_domain(self, domain):
        dl = [ord(x) for x in list(domain)]
        dl[0] = self._map_to_lowercase_letter(dl[0] + dl[3])
        dl[1] = self._map_to_lowercase_letter(dl[0] + 2*dl[1])
        dl[2] = self._map_to_lowercase_letter(dl[0] + dl[2] - 1)
        dl[3] =self._map_to_lowercase_letter(dl[1] + dl[2] + dl[3])
        return ''.join([chr(x) for x in dl])

    def generate_domain(self, count=None):
        if count:
            self.domaincount = count
        domains = []
        for seed in self.seed:
            domain = seed
            for i in range(round(self.domaincount/3)):
                domain = self._next_domain(domain=domain)
                domains = [*domains, domain]
        return list(set(domains))

#print(banjori().generate_domain())