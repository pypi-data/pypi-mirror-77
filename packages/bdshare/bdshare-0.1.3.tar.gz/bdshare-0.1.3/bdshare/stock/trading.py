import os
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from bdshare.util import vars as vs


def get_current_trade_data(symbol=None):
    """
        get last stock price.
        :param symbol: str, Instrument symbol e.g.: 'ACI' or 'aci'
        :return: dataframe
    """
    r = requests.get(vs.DSE_LSP_URL)
    #soup = BeautifulSoup(r.text, 'html.parser')
    soup = BeautifulSoup(r.content, 'html5lib')
    quotes = []  # a list to store quotes
    table = soup.find('table', attrs={
                      'class': 'table table-bordered background-white shares-table fixedHeader'})
    # print(table)
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        quotes.append({'symbol': cols[1].text.strip().replace(",", ""),
                       'ltp': cols[2].text.strip().replace(",", ""),
                       'high': cols[3].text.strip().replace(",", ""),
                       'low': cols[4].text.strip().replace(",", ""),
                       'close': cols[5].text.strip().replace(",", ""),
                       'ycp': cols[6].text.strip().replace(",", ""),
                       'change': cols[7].text.strip().replace("--", "0"),
                       'trade': cols[8].text.strip().replace(",", ""),
                       'value': cols[9].text.strip().replace(",", ""),
                       'volume': cols[10].text.strip().replace(",", "")
                       })
    df = pd.DataFrame(quotes)
    if symbol:
        df = df.loc[df.symbol == symbol.upper()]
        return df
    else:
        return df


def get_cse_current_trade_data(symbol=None):
    """
        get last stock price.
        :param symbol: str, Instrument symbol e.g.: 'ACI' or 'aci'
        :return: dataframe
    """
    r = requests.get(vs.CSE_LSP_URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    quotes = []  # a list to store quotes
    table = soup.find('table', attrs={'id': 'dataTable'})
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        quotes.append({'symbol': cols[1].text.strip().replace(",", ""),
                       'ltp': cols[2].text.strip().replace(",", ""),
                       'open': cols[3].text.strip().replace(",", ""),
                       'high': cols[4].text.strip().replace(",", ""),
                       'low': cols[5].text.strip().replace(",", ""),
                       'ycp': cols[6].text.strip().replace(",", ""),
                       'trade': cols[7].text.strip().replace(",", ""),
                       'value': cols[8].text.strip().replace(",", ""),
                       'volume': cols[9].text.strip().replace(",", "")
                       })
    df = pd.DataFrame(quotes)
    if symbol:
        df = df.loc[df.symbol == symbol.upper()]
        return df
    else:
        return df


def get_current_trading_code():
    """
        get last stock codes.
        :return: dataframe
    """
    r = requests.get(vs.DSE_LSP_URL)
    #soup = BeautifulSoup(r.text, 'html.parser')
    soup = BeautifulSoup(r.content, 'html5lib')
    quotes = []  # a list to store quotes
    table = soup.find('table')
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        quotes.append({'symbol': cols[1].text.strip().replace(",", "")})
    df = pd.DataFrame(quotes)
    return df


def get_hist_data(start=None, end=None, code='All Instrument'):
    """
        get historical stock price.
        :param start: str, Start date e.g.: '2020-03-01'
        :param end: str, End date e.g.: '2020-03-02'
        :param code: str, Instrument symbol e.g.: 'ACI'
        :return: dataframe
    """
    # data to be sent to post request
    data = {'startDate': start,
            'endDate': end,
            'inst': code,
            'archive': 'data'}

    r = requests.get(url=vs.DSE_DEA_URL, params=data)

    #soup = BeautifulSoup(r.text, 'html.parser')
    soup = BeautifulSoup(r.content, 'html5lib')

    quotes = []  # a list to store quotes

    table = soup.find('table', attrs={
                      'class': 'table table-bordered background-white shares-table fixedHeader'})
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        quotes.append({'date': cols[1].text.strip().replace(",", ""),
                       'symbol': cols[2].text.strip().replace(",", ""),
                       'ltp': cols[3].text.strip().replace(",", ""),
                       'high': cols[4].text.strip().replace(",", ""),
                       'low': cols[5].text.strip().replace(",", ""),
                       'open': cols[6].text.strip().replace(",", ""),
                       'close': cols[7].text.strip().replace(",", ""),
                       'ycp': cols[8].text.strip().replace(",", ""),
                       'trade': cols[9].text.strip().replace(",", ""),
                       'value': cols[10].text.strip().replace(",", ""),
                       'volume': cols[11].text.strip().replace(",", "")
                       })
    df = pd.DataFrame(quotes)
    if 'date' in df.columns:
        df = df.set_index('date')
        df = df.sort_index(ascending=False)
    else:
        print('No data found')
    return df


def get_basic_hist_data(start=None, end=None, code='All Instrument', index=None, retry_count=3, pause=0.001):
    """
        get historical stock price.
        :param start: str, Start date e.g.: '2020-03-01'
        :param end: str, End date e.g.: '2020-03-02'
        :param code: str, Instrument symbol e.g.: 'ACI'
        :param retry_count : int, e.g.: 3
        :param pause : int, e.g.: 0
        :return: dataframe
    """
    # data to be sent to post request
    data = {'startDate': start,
            'endDate': end,
            'inst': code,
            'archive': 'data'}

    for _ in range(retry_count):
        time.sleep(pause)
        try:
            r = requests.get(url=vs.DSE_DEA_URL, params=data)
        except Exception as e:
            print(e)
        else:
            #soup = BeautifulSoup(r.text, 'html.parser')
            soup = BeautifulSoup(r.content, 'html5lib')

            # columns: date, open, high, close, low, volume
            quotes = []  # a list to store quotes

            table = soup.find('table', attrs={
                              'class': 'table table-bordered background-white shares-table fixedHeader'})

            for row in table.find_all('tr')[1:]:
                cols = row.find_all('td')
                quotes.append({'date': cols[1].text.strip().replace(",", ""),
                               'open': float(cols[6].text.strip().replace(",", "")),
                               'high': float(cols[4].text.strip().replace(",", "")),
                               'low': float(cols[5].text.strip().replace(",", "")),
                               'close': float(cols[7].text.strip().replace(",", "")),
                               'volume': int(cols[11].text.strip().replace(",", ""))
                               })
            df = pd.DataFrame(quotes)
            if 'date' in df.columns:
                if (index == 'date'):
                    df = df.set_index('date')
                    df = df.sort_index(ascending=True)
                df = df.sort_index(ascending=True)
            else:
                print('No data found')
            return df


def get_close_price_data(start=None, end=None, code='All Instrument'):
    """
        get stock close price.
        :param start: str, Start date e.g.: '2020-03-01'
        :param end: str, End date e.g.: '2020-03-02'
        :param code: str, Instrument symbol e.g.: 'ACI'
        :return: dataframe
    """
    # data to be sent to post request
    data = {'startDate': start,
            'endDate': end,
            'inst': code,
            'archive': 'data'}

    r = requests.get(url=vs.DSE_CLOSE_PRICE_URL, params=data)

    #soup = BeautifulSoup(r.text, 'html.parser')
    soup = BeautifulSoup(r.content, 'html5lib')

    # columns: date, open, high, close, low, volume
    quotes = []  # a list to store quotes

    table = soup.find(
        'table', attrs={'class': 'table table-bordered background-white'})

    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        quotes.append({'date': cols[1].text.strip().replace(",", ""),
                       'symbol': cols[2].text.strip().replace(",", ""),
                       'close': cols[3].text.strip().replace(",", ""),
                       'ycp': cols[4].text.strip().replace(",", "")
                       })
    df = pd.DataFrame(quotes)
    if 'date' in df.columns:
        df = df.set_index('date')
        df = df.sort_index(ascending=False)
    else:
        print('No data found')
    return df
