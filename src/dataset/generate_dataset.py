"""
This module has class and methods needed for create DGA and benign domain data set
"""


class DgaDataset:
    """

    """
    def __init__(self, rec_count,method):
        """

        :param rec_count:
        :param method:
        """

 # create method for few algorithms
    def _althm1(self):
        pass


 # create method for few algorithms
    def _althm2(self):
        pass
    def dga_dataset(self,rec_count,method):
        """
        here call individual function and build data set and return as pd or save in CSV and return file name
        :param rec_count:
        :param method:
        :return:
        """


class BenignDataset:
    """

    """

    def __init__(self, rec_count, method):
        """

        :param rec_count:
        :param method:
        """

    # create method for few algorithms
    def _althm1(self):
        pass

    # create method for few algorithms
    def _althm2(self):
        pass

    def benign_dataset(self, rec_count, method):
        """
        here call individual function and build data set and return as pd or save in CSV and return file name
        :param rec_count:
        :param method:
        :return:
        """

if __name__ == "__main__":
    pd1=BenignDataset(rec_count=10000)
    pd2=DgaDataset(rec_count=10000)
    # concat pd and shuffle and save in CSV