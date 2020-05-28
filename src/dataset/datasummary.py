import os
import pandas as pd
import numpy as np
import glob


def summary(df):
    print(f" Before: Number of record {df.shape[0]} and number of columns {df.shape[1]}")
    df.drop_duplicates(keep="first", inplace=True)
    df.columns = ['domainName', 'family']
    df['label'] = 'bad'
    df.to_csv(OUTPUT_FILE, compression="gzip", mode='w',index=False)
    print("summary of data by family")
    print(f"After: Number of record {df.shape[0]} and number of columns {df.shape[1]}")
    print(df.groupby(['family']).agg(['count']))


if __name__=='__main__':
    OUTPUT_FILE = "{}/output/output.csv.gz".format(os.getenv('outputdir', "."))
    try:
        os.remove(OUTPUT_FILE)
    except OSError:
        pass
    file_list = glob.glob("./temp/*.csv")
    df = pd.DataFrame(data=np.empty((0,2)),columns=['domainName','family'])
    for file in file_list:
        try:
            df_temp = pd.read_csv(file)
            df_temp.columns = ['domainName', 'family']
            df= pd.concat([df,df_temp])
        except Exception as e:
            print(file)
            print(e)
            continue
    summary(df)
