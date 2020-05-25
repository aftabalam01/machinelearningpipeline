import string
import hashlib
import argparse
from datetime import datetime, timedelta


class Chinad:
    """

    """
    def __init__(self,date=datetime.now(),count=1000):
        self.generate_date = date
        self.domains = []
        self.domaincount = count
    def _dga(self, date=None):

        if date:
            self.generate_date = date


        TLDS = ['.com', '.org', '.net', '.biz', '.info', '.ru', '.cn']
        alphanumeric = string.ascii_lowercase + string.digits

        """
            Chinad generates 1000 domains, but only 256 different domains possible
        """

        for nr in range(0x100):
            data = "{}{}{}{}".format(
                    chr(date.year % 100),
                    chr(date.month),
                    chr(date.day),
                    chr(nr)) + 12*"\x00"

            h = hashlib.sha1(data.encode()).digest()
            h_le = []
            for i in range(5):
                for j in range(4):
                    h_le.append(h[i*4 + (3-j)])

            domain = ""
            for r in h_le[:16]:
                domain += alphanumeric[(r & 0xFF) % len(alphanumeric)]

            r = h_le[-4]
            domain += TLDS[r % len(TLDS)]
            yield domain

    def generate_domain(self,date=None):
        """

        :param date: datetime object
        :return:
        """
        if date:
            self.generate_date = date
        for c in range(round(self.domaincount/255)):
            for domain in self._dga(self.generate_date):
                self.domains = [*self.domains, domain]
            self.generate_date = self.generate_date - timedelta(days=1)
        return list(set(self.domains))

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="gozi dga")
#     parser.add_argument("-d", "--date",
#             help="date for which to generate domains")
#     args = parser.parse_args()
#     if args.date:
#         d = datetime.strptime(args.date, "%Y-%m-%d")
#     else:
#         d = datetime.now()
#
#     for domain in Chinad()._dga(d):
#         print(domain)
