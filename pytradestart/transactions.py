'''

'''
import os
import time
import glob
import datetime
import pandas as pd


def get_transactions(file):
    trans = pd.read_csv(file)
    trans = trans.rename(
        columns={
            'Detail': 'Details',
            'Credit ($)': 'Credit($)',
            'Debit ($)': 'Debit($)',
            'Balance ($)': 'Balance($)'
        })
    trans = trans.loc[trans.Details.str.startswith('B', na=False) | trans.Details.str.startswith('S', na=False)]
    trans.drop(trans.columns[-1], axis=1)
    trans["Qty"] = trans["Details"].str.split(' ').str[1]
    trans["Tick"] = trans["Details"].str.split(' ').str[2]
    trans["Price"] = trans["Details"].str.split(' ').str[4]
    trans["Type"] = (trans.apply(lambda x: 'Sell' if str.startswith(x["Details"], 'S') else "Buy", axis=1))
    trans['Date'] = pd.to_datetime(trans['Date'], format='%d/%m/%Y')
    trans.drop(trans.columns[5], axis=1, inplace=True)
    trans.sort_index(ascending=False, inplace=True)
    trans.sort_values('Date', ascending=False)
    return trans


def get_transaction_frame(data_path):
    ''' build a data frame from all transaction files'''
    pkl = f'{data_path}Transactions.pkl'
    df = None
    files = [f for f in glob.glob(data_path + 'Transactions*.csv')]
    for f in files:
        modified = time.ctime(os.path.getmtime(f))
        mod = datetime.datetime.strptime(modified, "%a %b %d %H:%M:%S %Y")
        print(mod.date())
        df = get_transactions(f)
        df = df.loc[:, ~df.columns.duplicated()]
        try:
            existing = pd.read_pickle(pkl)
            existing = existing.rename(
                columns={
                    'Detail': 'Details',
                    'Credit ($)': 'Credit($)',
                    'Debit ($)': 'Debit($)',
                    'Balance ($)': 'Balance($)'
                })
            drop_index = []
            for index, row in df.iterrows():
                has_existing = existing[existing['Reference'] == row['Reference']]
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
    df['index'] = df.index
    return df
