# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 22:39:24 2023

@author: Yigitalp
"""

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import os
from time import sleep
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
#Original Sandbox Environment: 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {'start': 1, 'limit': 15, 'convert': 'USD'}
headers = {'Accepts': 'application/json',
           'X-CMC_PRO_API_KEY': '0ad53085-1cb2-4eb8-ad9e-3ffbd7e56509'}
session = Session()
session.headers.update(headers)
try:
    response = session.get(url, headers=headers, params=parameters)
    data = json.loads(response.text)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

#print(type(data))

df = pd.json_normalize(data['data'])
df['timestamp'] = pd.Timestamp('now')

#%%
def api_runner():
    global df
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    #Original Sandbox Environment: 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {'start': 1, 'limit': 15, 'convert': 'USD'}
    headers = {'Accepts': 'application/json',
               'X-CMC_PRO_API_KEY': '0ad53085-1cb2-4eb8-ad9e-3ffbd7e56509'}
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, headers=headers, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    df2 = pd.json_normalize(data['data'])
    df2['timestamp'] = pd.Timestamp('now')
    df = pd.concat([df, df2])

    if not os.path.isfile(r'C:\Users\YİĞİTALP ÖZMEN\Desktop\CurriculumVitae(RESUME)\Documents\DATA ANALYTICS\Alex the Analyst Data Analyst Bootcamp\Python\Codebase\API.csv'):
        df.to_csv(r'C:\Users\YİĞİTALP ÖZMEN\Desktop\CurriculumVitae(RESUME)\Documents\DATA ANALYTICS\Alex the Analyst Data Analyst Bootcamp\Python\Codebase\API.csv', header='column_names')
    else:
        df.to_csv(r'C:\Users\YİĞİTALP ÖZMEN\Desktop\CurriculumVitae(RESUME)\Documents\DATA ANALYTICS\Alex the Analyst Data Analyst Bootcamp\Python\Codebase\API.csv', mode='a', header=False)


for i in range(2):  # make it 333
    api_runner()
    print('API runner completed')
    sleep(60)  # sleep for 1 minute

#%%
df_api = pd.read_csv('API.csv')
df_api.info()
df_api_grouped = df_api.groupby(by='name', sort=False)['quote.USD.percent_change_1h',
                                                       'quote.USD.percent_change_24h',
                                                       'quote.USD.percent_change_7d',
                                                       'quote.USD.percent_change_30d',
                                                       'quote.USD.percent_change_60d',
                                                       'quote.USD.percent_change_90d'].mean()

df_api_grouped_stacked = df_api_grouped.stack()
df_api_grouped_stacked = df_api_grouped_stacked.to_frame(name='values')
df_api_grouped_stacked = df_api_grouped_stacked.reset_index()
df_api_grouped_stacked = df_api_grouped_stacked.rename(
    columns={'level_1': 'percent_change'})


df_api_grouped_stacked['percent_change'] = df_api_grouped_stacked['percent_change'].replace(['quote.USD.percent_change_1h',
                                                                                             'quote.USD.percent_change_24h',
                                                                                             'quote.USD.percent_change_7d',
                                                                                             'quote.USD.percent_change_30d',
                                                                                             'quote.USD.percent_change_60d',
                                                                                             'quote.USD.percent_change_90d'], ['1h', '24h', '7d', '30d', '60d','90d'])
                                                                                                                               
                                                                                                                               
                                                                                                                               

plt.style.use('ggplot')
matplotlib.rcParams['figure.figsize'] = (12, 8)
sns.catplot(x='percent_change', y='values', hue='name',
            data=df_api_grouped_stacked, kind='point')

#%%
df_api_grouped_stacked_specific = df_api[['name', 'quote.USD.price', 'timestamp']]
df_api_grouped_stacked_specific = df_api_grouped_stacked_specific.query("name == 'Bitcoin'")
sns.lineplot(x='timestamp', y='quote.USD.price', data=df_api_grouped_stacked_specific)