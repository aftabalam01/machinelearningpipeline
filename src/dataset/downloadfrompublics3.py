import pandas as pd
from urllib.request import urlretrieve
# url= 'https://benigndomains.s3.amazonaws.com/'
# df_benign = pd.DataFrame()
# for i in range(841,2863,1):
#     filename = f'benign{i}.csv'
#     file_name, headers = urlretrieve(url = f'{url}{filename}',filename=filename)
#     try:
#         df = pd.read_csv(file_name)
#         df_benign = pd.concat([df_benign,df])
#     except:
#         df_benign.to_csv("rapid7_benign_dataset.csv.gz", compression="gzip", mode='a')
#         pass

df = pd.read_csv("rapid7_benign_dataset.csv.zip")

df.head()
df.count()
df.drop_duplicates(keep='first',inplace=True)
df.count()