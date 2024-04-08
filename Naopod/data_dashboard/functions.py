import MetaTrader5 as mt
import pandas as pd
from datetime import datetime

def get_ohlc(symbol):

    df= pd.DataFrame(mt.copy_rates_from_pos(symbol, 
                                                mt.TIMEFRAME_M5, 
                                                1, 
                                                300))

    df['time'] = pd.to_datetime(df['time'], unit='s')
    df = df[['time', 'open', 'high', 'low', 'close', 'tick_volume']]
    df.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']

    df.set_index('Datetime', inplace=True)

    return df

def get_obaw_data():

    df = pd.DataFrame(mt.history_deals_get(datetime(2023,8,12), datetime.now()))
    df.rename(columns={2: 'Time', 13: 'Profits', 15:'Symbol'}, inplace=True)
    df['Time'] = pd.to_datetime(df['Time'], unit='s')
    # Dropping deposits rows
    df = df[df[7] != 0]
    # Keeping only end of trade data
    df = df.loc[df['Profits'] != 0]

    ## Statistics

    return df
    



    
