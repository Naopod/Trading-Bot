import MetaTrader5 as mt
import pandas as pd
from indicators_opti import FDI
from datetime import datetime, timedelta
from strategies_opti import DivergenceIchimoku, SuperTrends, ChandelierExitsZlsma
import warnings
from pandas.errors import SettingWithCopyWarning

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

'''Data for the graph'''

def GetData(symbol):

    # Extract data we want to work on, using different timeframes
    df_M30 = pd.DataFrame(mt.copy_rates_from_pos(symbol, mt.TIMEFRAME_M30, 1, 10000))
    df_M15 = pd.DataFrame(mt.copy_rates_from_pos(symbol, mt.TIMEFRAME_M15, 1, 20000))
    df_M5 = pd.DataFrame(mt.copy_rates_from_pos(symbol, mt.TIMEFRAME_M5, 1, 50000))

    # Clear up data
    df_M30['time'] = pd.to_datetime(df_M30['time'], unit='s')
    df_M30 = df_M30[['time', 'open', 'high', 'low', 'close', 'tick_volume']]
    df_M30.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
    df_M30.set_index('Datetime', inplace=True)

    df_M15['time'] = pd.to_datetime(df_M15['time'], unit='s')
    df_M15 = df_M15[['time', 'open', 'high', 'low', 'close', 'tick_volume']]
    df_M15.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
    df_M15.set_index('Datetime', inplace=True)

    df_M5['time'] = pd.to_datetime(df_M5['time'], unit='s')
    df_M5 = df_M5[['time', 'open', 'high', 'low', 'close', 'tick_volume']]
    df_M5.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
    df_M5.set_index('Datetime', inplace=True)

    # Calculate fdi
    df_M30['fdi'] = df_M30['Close'].rolling(window=14).apply(FDI)
    df_M15['fdi'] = df_M15['Close'].rolling(window=14).apply(FDI)
    df_M5['fdi'] = df_M5['Close'].rolling(window=14).apply(FDI)

    return df_M30, df_M15, df_M5

