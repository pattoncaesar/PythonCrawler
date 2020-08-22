import time
from io import StringIO
import requests
import pandas as pd
import pickle

def create_today_timestamp():
    today = time.strftime("%Y-%m-%d",time.gmtime())
    return int(time.mktime(time.strptime(today, "%Y-%m-%d")))
def create_timestamp_from_today(n):
    today = create_today_timestamp()
    return today + n*24*3600
tomorrow_timestamp = create_timestamp_from_today(1)
# print(tomorrow_timestamp)

def create_tw_stock_info_list():
    res = requests.get("http://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
    df = pd.read_html(res.text)[0]
    df.columns = df.iloc[0]
    # print(df.columns)
    df = df.iloc[2:]
    # print(df)
    df = df.dropna(thresh=3, axis=0).dropna(thresh=3, axis=1)
    # print(df)
    df = df.dropna(how='all')
    # print(df)
    df = df.reset_index(drop=True)
    new_df = df['有價證券代號及名稱'].str.replace(u'\u3000',' ').str.split(u' ',expand=True)
    # print(new_df)
    new_df.columns = ['Ticker', 'StockName', 'Sector']
    new_df['Sector'] = df['產業別']
    # print(new_df)
    return new_df
tw_stock_info_df = create_tw_stock_info_list()
# print(tw_stock_info_df)


stock_df = pd.DataFrame()
# ticker_list = tw_stock_info_df['Ticker']
ticker_list = tw_stock_info_df['Ticker'].head(30)
for ticker in ticker_list:
    print('## Info: Download Ticker ' + ticker + '!')
    site = "https://query1.finance.yahoo.com/v7/finance/download/" + ticker + ".TW?period1=0&period2=" + str(
        tomorrow_timestamp) + "&interval=1d&events=history&crumb=hP2rOschxO0"
    try:
        response = requests.get(site)
        # print(response)
        tmp_df = pd.read_csv(StringIO(response.text))
        # print(tmp_df)
        tmp_df['Ticker'] = ticker
        stock_df = pd.concat([stock_df, tmp_df], axis=0)
    except:
        print('## Warning: Ticker ' + ticker + ' is failed!')

stock_df = stock_df.reset_index(drop=True)
stock_df = stock_df[['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
print(stock_df)
# https://query1.finance.yahoo.com/v7/finance/download/2330.TW?period1=0&period2=1598112000&interval=1d&events=history&crumb=hP2rOschxO0
# https://query1.finance.yahoo.com/v7/finance/download/2330.TW?period1=0&period2=1549258857&interval=1d&events=history&crumb=hP2rOschxO0