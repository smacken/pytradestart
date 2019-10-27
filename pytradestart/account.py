'''

'''
import os
import time
import glob
import datetime
import pandas as pd


def get_dividends(df):
    ''' get dividends from transaction frame '''
    div = df[df['Details'].str.contains('Direct Credit') | df['Details'].str.contains('Credit Interest')]
    div = div[div['Details'].str.contains('COMMONWEALTH') is False]
    div["Symbol"] = div["Details"].str.split(' ').str[3]
    df['Date'] = df['Date'].astype('datetime64[ns]')
    df = df.reindex(index=df.index[::-1])
    df['Sum'] = df['Amount'].cumsum()
    return div


def get_account_transactions(file):
    columns = ['Date', 'Amount', 'Details', 'Balance']
    account = pd.read_csv(file, header=None, names=columns, dayfirst=True, parse_dates=['Date'])
    return account


def get_account_frame(data_path):
    files = [f for f in glob.glob(f'{data_path}Account*.csv')]
    df = None
    for f in files:
        modified = time.ctime(os.path.getmtime(f))
        mod = datetime.datetime.strptime(modified, "%a %b %d %H:%M:%S %Y")
        print(mod.date())
        df = get_account_transactions(f)
        pkl = f'{data_path}Account.pkl'
        try:
            existing = pd.read_pickle(pkl)
            drop_index = []
            for index, row in df.iterrows():
                has_existing = existing[(existing['Date'] == row['Date']) & (existing['Amount'] == row['Amount'])]
                if has_existing.empty:
                    continue
                drop_index.append(index)
            if len(drop_index) > 0:
                df.drop(drop_index, inplace=True)
            df = df.append(existing, ignore_index=True)
        except Exception as e:
            print('no pkl exists', str(e))
        df.to_pickle(pkl)

    df = df.sort_values(by=['Date'], ascending=False)
    return df
