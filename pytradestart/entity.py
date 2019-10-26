'''

'''
import sys
import os
import os.path, time
import glob
import datetime
import pandas as pd
import numpy as np
import csv
import featuretools as ft
import pyasx
import pyasx.data.companies

def get_entityset(holding_data, price_data, trans_data, company_data):
    ''' Construct an entityset data model from different data frames '''

    company_data = company_data.drop(['listing_date', 'delisting_date', 'last_trade_date', 'indices'], axis=1)

    es = ft.EntitySet(id="trading")
    es = es.entity_from_dataframe(entity_id="prices",
                                    dataframe=price_data,
                                    time_index="Date",
                                    index='index',
                                    variable_types={"Tick": ft.variable_types.Categorical})
    es = es.entity_from_dataframe(entity_id="holdings",
                                    dataframe=holding_data,
                                    index='Tick',
                                    time_index="Date",
                                    variable_types={"Tick": ft.variable_types.Categorical})
    es = es.entity_from_dataframe(entity_id="companies",
                                    dataframe=company_data,
                                    index='index',
                                    time_index="Date",
                                    variable_types={"Tick": ft.variable_types.Categorical})
    es = es.entity_from_dataframe(entity_id="transactions",
                                    dataframe=trans_data,
                                    index='index',
                                    time_index="Date",
                                    variable_types={"Tick": ft.variable_types.Categorical, 
                                                    "Type": ft.variable_types.Categorical})
    holdings_trans = ft.Relationship(es["holdings"]["Tick"], es["transactions"]["Tick"])
    es = es.add_relationship(holdings_trans)
    holdings_companies = ft.Relationship(es["holdings"]["Tick"], es["companies"]["Tick"])
    es = es.add_relationship(holdings_companies)
    holdings_prices = ft.Relationship(es["holdings"]["Tick"], es["prices"]["Tick"])
    es = es.add_relationship(holdings_prices)
    return es
