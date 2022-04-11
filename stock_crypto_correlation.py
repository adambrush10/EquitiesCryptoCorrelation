import requests 
import json
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import date
from scipy.stats import pearsonr
import statistics
import math
import streamlit as st

##################################################################
#create venv -- python3 -m venv env
#run venv --  .\env\Scripts\activate
# leave venv -- deactivate 
##################################################################

                    #       inputs      #


### CRYPTO ##########################
                                    #
exchange = "coinbase-pro"           #
#pair = "btcusd"                     #
                                    #
#####################################


############    Date Parameters    ##############################
                                                                #
START_DATE = '1/1/2022'                                         #
END_DATE = '4/5/2022'                                           #
PERIOD = 86400  # Time period in seconds (e.g., 1 day = 86400)  #
                                                                #
#################################################################


###     Stocks     ##############################################
                                                                #
#symbol = 'QQQ'                                                  #
                                                                #
#################################################################



# BELOW ARE ALL FUNCTIONS THAT ARE CALLED IN MAIN.PY

# Convert the dates to timestamps
def to_timestamp(dateString):
    #element = datetime.strptime(dateString, '%m/%d/%Y')
    element = date.strftime(dateString, '%Y/%m/%d')
    element = datetime.strptime(element, '%Y/%m/%d')
    return int(datetime.timestamp(element))

# Will be used later to convert back
def to_date(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%m/%d/%Y')

def to_backward_date(dateString):
    element = date.strftime(dateString, '%Y/%m/%d')
    element = datetime.strptime(dateString, '%m/%d/%Y')
    return datetime.strftime(element, "%Y-%m-%d")

#start_ts = to_timestamp(START_DATE)
#end_ts = to_timestamp(END_DATE)


# cryptowat.ch API     -- historical data for Crypto protocols on a variety of exchanges 
# docs found here      -- https://docs.cryptowat.ch/rest-api/
def cryptowatchAPIcall(option, START_DATE, END_DATE):
    start_ts = to_timestamp(START_DATE)
    end_ts = to_timestamp(END_DATE)

    params = {
        "after": start_ts,
        "before": end_ts,
        "periods": PERIOD,
    }
    pricefeed = requests.get(
    f'https://api.cryptowat.ch/markets/{exchange}/{option}/ohlc',
    params=params)
    crypto_price = pricefeed.json()
    return crypto_price

def json_to_df(cryptowat, option, START_DATE, END_DATE):
    funcinput = cryptowat
    day_count = len(funcinput["result"]["86400"])
    print(f"Retrieving historical prices for {option} from {exchange}")
    print(f"between {START_DATE} and {END_DATE}")
    print(f'Analyzing {day_count} total days')
    daily_resp = funcinput["result"]["86400"]
    O =[] 
    H=[]
    L=[]
    C=[]
    vol=[]
    date=[]
    weekday=[]
    new_date = []
    count = 0
    
    #populate all lists from json response
    while count < day_count:
        date.append(daily_resp[count][0])
        O.append(daily_resp[count][1])
        H.append(daily_resp[count][2])
        L.append(daily_resp[count][3])
        C.append(daily_resp[count][4])
        vol.append(daily_resp[count][5])
        if count > day_count:
            break
        count = count + 1
    
    #get day of week (1 = Mon, 2 = Tues, 3 = Wed,... 7 = Sun)
    for x in date:
        wkdy = datetime.fromtimestamp(x).strftime("%A")
        weekday.append(wkdy)
        
    #convert unix date to readable date
    for x in date:
        new = to_date(x)
        new_date.append(new)
        
    #create DataFrame    
    df = pd.DataFrame()
    df["Date"] = new_date
    df["Open"] = O
    df["High"] = H
    df["Low"] = L
    df["Close"] = C
    df["Volume"] = vol
    df["Weekday"] = weekday
    df["log_return"] = np.log(df.Close) - np.log(df.Close.shift(1))
    # df.set_index(["Date"])
    return df
    
def PolygonAPIcall(symbol, START_DATE, END_DATE):
    new_start_date = START_DATE
    new_end_date = END_DATE
    apiKey = "ALb57Y72t3B2f3zVIAKUeaGMT4M2vzL9"
    date_from = START_DATE    #removed backward date function call 
    date_to = END_DATE     #removed backward date function call 
    response2 = requests.get(f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{date_from}/{date_to}?adjusted=true&sort=asc&limit=600&apiKey=ALb57Y72t3B2f3zVIAKUeaGMT4M2vzL9")
    stock_price = response2.json()
    return stock_price

def json_to_df2(poly, symbol, START_DATE, END_DATE):
    call2= poly
    print(call2)
    O = []
    H = []
    L = []
    C = []
    weekday=[]
    date = []
    vol = []
    newdate= []
    day_count = len(call2["results"])
    day_count
    print(f"Retrieving historical prices for {symbol}")
    print(f"between {START_DATE} and {END_DATE}")
    print(f'Analyzing {day_count} total days')
    count = 0
    while count < day_count:
        date.append(call2["results"][count]["t"])
        O.append(call2["results"][count]["o"])
        H.append(call2["results"][count]["h"])
        L.append(call2["results"][count]["l"])
        C.append(call2["results"][count]["c"])
        vol.append(call2["results"][count]["v"])
        if count > day_count:
            break
        count = count+1
        
    #convert unix date to readable date
    for x in date:
        x = x/1000
        new = to_date(x)
        newdate.append(new)
        
    #get day of week 
    for x in date:
        wkdy = datetime.fromtimestamp(x/1000).strftime("%A")
        weekday.append(wkdy)
        
    #create DataFrame    
    df2 = pd.DataFrame()
    df2["Date"] = newdate
    df2["Open"] = O
    df2["High"] = H
    df2["Low"] = L
    df2["Close"] = C
    df2["Volume"] = vol
    df2["Weekday"] = weekday
    df2["log_return"] = np.log(df2.Close) - np.log(df2.Close.shift(1))
    #df2.set_index(["Date"])
    return df2


def combineLinechart(crypto, stock, option, symbol):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Add traces
    fig.add_trace(
        go.Scatter(x=crypto["Date"], y=crypto["Close"], name=option),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=stock["Date"], y=stock["Close"], name=symbol),
        secondary_y=True,
    )
    fig.update_xaxes(
        dtick=7,
        tickformat="%b")
    fig.update_layout(
        title = "Equities vs Crypto Comparison",
        template="plotly_dark")
    
    return fig


def logLinechart(crypto, stock, option, symbol):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Add traces
    fig.add_trace(
        go.Scatter(x=crypto["Date"], y=crypto['log_return'], name=option),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=stock["Date"], y=stock['log_return'], name=symbol),
        secondary_y=True,
    )
    fig.update_xaxes(
        dtick=7,
        tickformat="%b")
    fig.update_layout(
        title = "Logarithmic Returns",
        template="plotly_dark")
    
    return fig


def PearsonCorrValue(crypto,stock):
    dfcorr = pd.DataFrame()
    dfcorr["crypto_log"] = crypto['log_return']
    dfcorr = dfcorr.set_index(crypto['Date'])
    
    dfcorr2 = pd.DataFrame()
    dfcorr2["stock_log"] = stock['log_return']
    dfcorr2["date"] = stock['Date']
    #dfcorr2 = dfcorr2.set_index(df2['Date'])
    
    dfcorr3 = pd.merge(dfcorr, dfcorr2, left_index=True, right_on='date')
    dfcorr3 = dfcorr3.set_index("date")
    dfcorr3 = dfcorr3.corr()
    return dfcorr3
    
#GET ROLLING CORRELATION (DEFAULT 20 days) OUTPUT LINE CHART 

def ROLLINGcorrelation(crypto,stock):
    dfcorr = pd.DataFrame()
    dfcorr["crypto_log"] = crypto['log_return']
    dfcorr = dfcorr.set_index(crypto['Date'])
    
    dfcorr2 = pd.DataFrame()
    dfcorr2["stock_log"] = stock['log_return']
    dfcorr2["date"] = stock['Date']
    #dfcorr2 = dfcorr2.set_index(df2['Date'])
    
    dfcorr3 = pd.merge(dfcorr, dfcorr2, left_index=True, right_on='date')
    dfcorr3 = dfcorr3.set_index("date")
    #dfcorr3 = dfcorr3.corr()
    
    fig1 = dfcorr3['crypto_log'].rolling(window=20).corr(dfcorr3['stock_log'])
    #ax.axhline(df2["log_return"].corr().iloc[0,1], c='r')
    
    return fig1.plot(figsize=(14,6))    


#calculate rolling weekly vol Crypto (7 day rolling)

def RollingVolCrypto(crypto):
    #calculate Vol
    st_dev = crypto['log_return'].std()
    print(f'The Average vol for any given day is {st_dev}')
    volatility = crypto['log_return'].std()*365**.5
    print(f'{volatility} vol asset in the given period')
    crypto['weekly_vol'] = crypto['log_return'].rolling(window=7).std()*7**.5
    
    fig = px.line(crypto, x=crypto["Date"], y=crypto["weekly_vol"], title='Weekly Rolling Volatility')
    fig.update_xaxes(
        dtick=7,
        tickformat="%b")
    fig.update_layout(
        title = "Weekly Rolling Volatility",
        template="plotly_dark")
    #fig.show()
    
    return fig


def messariCryptoAPI(proj):
    token = proj
    url = f"https://data.messari.io/api/v1/assets/{token}/metrics"
    response = requests.get(url)
    response = response.json()
    name = response["data"]['name']
    symbol = response["data"]['symbol']
    mcap = response["data"]["marketcap"]['current_marketcap_usd']
    price = response['data']["market_data"]['price_usd']
    day = response['data']["market_data"]['percent_change_usd_last_24_hours']
    month = response["data"]['roi_data']['percent_change_last_1_month']
    month3 = response["data"]['roi_data']['percent_change_last_3_months']
    year = response["data"]['roi_data']['percent_change_last_1_year']
    dict = {
    "Name": name,
    "Symbol": symbol,
    "marketcap": mcap,
    "Price": price,
    "24hr % Change": day,
    "1mo % Change": month,
    "3mo % Change": month3,
    "1 Year % Change": year
    }
    StatisticsDF = pd.DataFrame.from_dict(dict, orient="index")
    StatisticsDF = StatisticsDF.astype('str')
    print(StatisticsDF.dtypes)
    #StatisticsDF = StatisticsDF.rename(columns={0: "Statistics"})
    print(StatisticsDF)
    return StatisticsDF

