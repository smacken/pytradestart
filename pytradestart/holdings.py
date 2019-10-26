'''

'''
import os
import time
import glob
import datetime
import pandas as pd
import csv


def get_holdings(file):
    '''
    holdings can come from export or data feed (simple)
    '''
    simple_csv = False
    with open(file, encoding="utf8") as csvfile:
        hold = csv.reader(csvfile, delimiter=',', quotechar='|')
        line_count = 0
        for row in hold:
            if line_count == 1:
                break
            if 'Code' in row:
                simple_csv = True
            line_count += 1
    if simple_csv:
        holdings = pd.read_csv(file, header=0)
    else:
        holdings = pd.read_csv(file, skiprows=[0, 1, 3], header=0)
        cols = [9, 10]
        holdings.drop(holdings.columns[cols], axis=1, inplace=True)
        holdings = holdings[:-4]
        holdings = holdings.rename(columns={
            'Purchase($)': 'Purchase $', 
            'Last($)': 'Last $', 
            'Mkt Value($)': 'Mkt Value $',
            'Profit / Loss($)': 'Profit/Loss $',
            'Profit / Loss(%)': 'P/L %',
            'Change($)': 'Change $',
            'Chg Value($)':'Value Chg $'
        })
    return holdings
    
def get_holdings_frame(data_path):
    ''' get holdings along a time series '''
    pkl = data_path + 'Holdings.pkl'
    df = None
    holdings_files = [f for f in glob.glob(data_path + 'Holdings*.csv')]
    for f in holdings_files:
        modified = time.ctime(os.path.getmtime(f))
        mod = datetime.datetime.strptime(modified, "%a %b %d %H:%M:%S %Y")
        #print(f)
        df = get_holdings(f)
        df['Date'] = mod.date()
        if 'Code' in df.columns:
            df = df.rename(columns={'Code': 'Tick'})
        df = df[df['Avail Units'].notnull()]
        
        existing = pd.read_pickle(pkl) if os.path.isfile(pkl) else pd.DataFrame() 
        try:
            has_holdings = existing[existing['Date'] == mod.date()] if not existing.empty else None
            if not existing.empty and has_holdings.Tick.count() > 0:
                continue
            df = df.append(existing, ignore_index=True)
            df.to_pickle(pkl)
        except Exception as ex:
            print('no pkl exists', str(ex))
        
    df = df.sort_values(by=['Date', 'Tick'], ascending=False)
    return df

def holdings(data_path, latest=True):
    ''' get the pickled holding data set '''
    holding = pd.read_pickle(f'{data_path}Holdings.pkl')
    holding['index'] = holding.index
    return holding if not latest else holding[holding.Date == holding.Date.max()]
