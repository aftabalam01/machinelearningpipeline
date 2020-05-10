import os
import pandas as pd

def summary(df):
    df.drop_duplicates(keep="first", inplace=True)
    df.columns = ['domainName', 'family']
    df['label'] = 'bad'
    df.to_csv(OUTPUT_FILE, compression="gzip", mode='w',index=False)
    print("summary of data by family")
    print(df.groupby(['family']).agg(['count']))


if __name__=='__main__':
    INPUT_FILE= "{}/processingdata.csv.gz".format(os.getenv('datadir',"."))
    OUTPUT_FILE = "{}/output/output.csv.gz".format(os.getenv('datadir', "."))
    try:
        os.remove(OUTPUT_FILE)
    except OSError:
        pass
    df = pd.read_csv(INPUT_FILE)
    summary(df)
