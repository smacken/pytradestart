'''

'''
import pandas as pd


def get_price_frame(data_path):
    ''' get price time-series ticker data ohlc '''
    price_data = pd.read_pickle(f'{data_path}Prices.pkl')
    price_data.drop_duplicates(subset=['Date', 'Tick'], keep='first', inplace=True)
    price_data['index'] = price_data.index
    return price_data


def get_companies_frame(data_path):
    ''' company details data frame '''

    etf_data = f'{data_path}etf.json'
    etf = pd.read_json(etf_data)
    etf = etf.loc[1:]
    etf_codes = etf['ASX Code'].tolist()

    company_pkl = f'{data_path}Companies.pkl'
    trans_pkl = f'{data_path}Transactions.pkl'
    trans = pd.read_pickle(trans_pkl)
    company_frame = None

    for tick in trans.Tick.unique().tolist():
        if tick in etf_codes:
            continue

        try:
            company = pd.read_pickle(company_pkl)
            company.rename(columns={'ticker': 'Tick'}, inplace=True)
        except Exception as ex:
            print(ex)
            # company_info = pyasx.data.companies.get_company_info(tick)
            company_info = {}
            company = pd.DataFrame([company_info])
            company.rename(columns={'ticker': 'Tick'}, inplace=True)
            share = pd.DataFrame([company_info['primary_share']])
            share.rename(columns={'ticker': 'Tick'}, inplace=True)
            company = company.merge(share, on='Tick')
            company['Date'] = pd.to_datetime('today')
  
        if company[company.Tick == tick].empty:
            # company_info = pyasx.data.companies.get_company_info(tick)
            company_info = {}
            company_df = pd.DataFrame([company_info])
            company_df.rename(columns={'ticker': 'Tick'}, inplace=True)
            share = pd.DataFrame([company_info['primary_share']])
            share.rename(columns={'ticker': 'Tick'}, inplace=True)
            company_df = company_df.merge(share, on='Tick')
            company_df['Date'] = pd.to_datetime('today')
            company = company.append(company_df)
            company_frame = company if company_frame is None or company_frame.empty else company_frame.append(company)
        else:
            company_frame = company if company_frame is None else company_frame.append(company)

    company_frame.drop_duplicates(['Tick', 'Date'], keep='first', inplace=True)
    company_frame.rename(columns={'Tick': 'Tick'}, inplace=True)
    company_frame['Date'] = company_frame['Date'].apply(lambda x: x if not pd.isnull(x) else pd.to_datetime('today'))
    company_frame['DateIndex'] = company_frame['Date'].apply(lambda x: x.strftime('%y-%m-%d'))
    company_frame = company_frame.reset_index(drop=True)
    company_frame['index'] = company_frame.index
    company_frame.to_pickle(company_pkl)
    return company_frame
