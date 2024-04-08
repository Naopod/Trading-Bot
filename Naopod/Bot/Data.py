import MetaTrader5 as mt
import pandas as pd
from datetime import datetime
from Indicators import FDI
from Strategies import DivergenceIchimoku, SuperTrends, ChandelierExitsZlsma
import warnings
from pandas.errors import SettingWithCopyWarning

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

'''Import data from MetaTrader5 and merged it'''

def GetData(symbol, timeframe):

    
    ## Extract data we want to work on, using different timeframes

    if timeframe == 'M5':

        df= pd.DataFrame(mt.copy_rates_from_pos(symbol, 
                                                mt.TIMEFRAME_M5, 
                                                1, 
                                                300))
        
    
    elif timeframe == 'M30':
        
        df = pd.DataFrame(mt.copy_rates_from_pos(symbol, 
                                            mt.TIMEFRAME_M30, 
                                            1, 
                                            350))

    elif timeframe == 'M15':

        df = pd.DataFrame(mt.copy_rates_from_pos(symbol, 
                                                mt.TIMEFRAME_M15, 
                                                1, 
                                                300)) 
    else:
        raise ValueError("Invalid timeframe: " + timeframe)

    
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df = df[['time', 'open', 'high', 'low', 'close', 'tick_volume']]
    df.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']

    df.set_index('Datetime', inplace=True)
    df['fdi'] = df['Close'].rolling(window=14).apply(FDI)

    return df

def MergedDF(symbol, timeframe):

    ## Create copies for the strategies

    df = GetData(symbol, timeframe)

    df_1 = df.copy()
    df_2 = df.copy()
    df_3 = df.copy()

    ## Call strategies

    if timeframe == 'M30':

        if symbol == 'EURUSD':

            df_1 = DivergenceIchimoku(df_1, timeframe='M30', n_rsi=24, tolerance=6) 

            df_2 = SuperTrends(df_2, timeframe='M30', ema=160, per_m5=14, per_m15=14, per_m30=17, atr_mul_m5=2, atr_mul_m15=4, atr_mul_m30=5)

            df_3 = ChandelierExitsZlsma(df_3, timeframe='M30', zlsma=25, ce_mult=4)

            df_3.rename(columns={'signal':'signal_3'}, inplace=True)
            df_3.rename(columns={'sl':'sl_3'}, inplace=True)
            df_3.rename(columns={'tp_1':'tp_3_1'}, inplace=True)
            df_3.rename(columns={'tp_2':'tp_3_2'}, inplace=True)
            df_3.rename(columns={'tp_3':'tp_3_3'}, inplace=True)
            df_3.rename(columns={'tp_4':'tp_3_4'}, inplace=True)
            df_3.rename(columns={'tp_5':'tp_3_5'}, inplace=True)
            df_2.rename(columns={'signal':'signal_2'}, inplace=True)
            df_2.rename(columns={'sl':'sl_2'}, inplace=True)
            df_2.rename(columns={'tp_1':'tp_2_1'}, inplace=True)
            df_2.rename(columns={'tp_2':'tp_2_2'}, inplace=True)
            df_2.rename(columns={'tp_3':'tp_2_3'}, inplace=True)
            df_2.rename(columns={'tp_4':'tp_2_4'}, inplace=True)
            df_2.rename(columns={'tp_5':'tp_2_5'}, inplace=True)
            df_1.rename(columns={'signal':'signal_1'}, inplace=True)
            df_1.rename(columns={'sl':'sl_1'}, inplace=True)
            df_1.rename(columns={'tp_1':'tp_1_1'}, inplace=True)
            df_1.rename(columns={'tp_2':'tp_1_2'}, inplace=True)
            df_1.rename(columns={'tp_3':'tp_1_3'}, inplace=True)
            df_1.rename(columns={'tp_4':'tp_1_4'}, inplace=True)
            df_1.rename(columns={'tp_5':'tp_1_5'}, inplace=True)

            grosses_couilles = df_1.merge(df_2[['signal_2', 'sl_2', 'tp_2_1', 'tp_2_2', 'tp_2_3', 'tp_2_4', 'tp_2_5']], left_index=True, right_index=True, how='left') \
            .merge(df_3[['signal_3', 'sl_3', 'tp_3_1', 'tp_3_2', 'tp_3_3', 'tp_3_4', 'tp_3_5']], left_index=True, right_index=True, how='left') \
        
        elif symbol == 'GBPUSD':

            df_1 = DivergenceIchimoku(df_1, timeframe='M30', n_rsi=14, tolerance=5) 

            df_2 = SuperTrends(df_2, timeframe='M30', ema=270, per_m5=11, per_m15=12, per_m30=16, atr_mul_m5=2, atr_mul_m15=4, atr_mul_m30=5)

            df_3 = ChandelierExitsZlsma(df_3, timeframe='M30', zlsma=25, ce_mult=3)

            df_3.rename(columns={'signal':'signal_3'}, inplace=True)
            df_3.rename(columns={'sl':'sl_3'}, inplace=True)
            df_3.rename(columns={'tp_1':'tp_3_1'}, inplace=True)
            df_3.rename(columns={'tp_2':'tp_3_2'}, inplace=True)
            df_3.rename(columns={'tp_3':'tp_3_3'}, inplace=True)
            df_3.rename(columns={'tp_4':'tp_3_4'}, inplace=True)
            df_3.rename(columns={'tp_5':'tp_3_5'}, inplace=True)
            df_2.rename(columns={'signal':'signal_2'}, inplace=True)
            df_2.rename(columns={'sl':'sl_2'}, inplace=True)
            df_2.rename(columns={'tp_1':'tp_2_1'}, inplace=True)
            df_2.rename(columns={'tp_2':'tp_2_2'}, inplace=True)
            df_2.rename(columns={'tp_3':'tp_2_3'}, inplace=True)
            df_2.rename(columns={'tp_4':'tp_2_4'}, inplace=True)
            df_2.rename(columns={'tp_5':'tp_2_5'}, inplace=True)
            df_1.rename(columns={'signal':'signal_1'}, inplace=True)
            df_1.rename(columns={'sl':'sl_1'}, inplace=True)
            df_1.rename(columns={'tp_1':'tp_1_1'}, inplace=True)
            df_1.rename(columns={'tp_2':'tp_1_2'}, inplace=True)
            df_1.rename(columns={'tp_3':'tp_1_3'}, inplace=True)
            df_1.rename(columns={'tp_4':'tp_1_4'}, inplace=True)
            df_1.rename(columns={'tp_5':'tp_1_5'}, inplace=True)

            grosses_couilles = df_1.merge(df_2[['signal_2', 'sl_2', 'tp_2_1', 'tp_2_2', 'tp_2_3', 'tp_2_4', 'tp_2_5']], left_index=True, right_index=True, how='left') \
            .merge(df_3[['signal_3', 'sl_3', 'tp_3_1', 'tp_3_2', 'tp_3_3', 'tp_3_4', 'tp_3_5']], left_index=True, right_index=True, how='left')       
        
    elif timeframe == 'M15':

        if symbol == 'EURUSD':

            df_1 = DivergenceIchimoku(df_1, timeframe='M15', n_rsi=18, tolerance=1)
            df_2 = SuperTrends(df_2, timeframe='M15', ema=230, per_m5=10, per_m15=13, per_m30=17, atr_mul_m5=1, atr_mul_m15=5, atr_mul_m30=5)
            df_3 = ChandelierExitsZlsma(df_3, timeframe='M15', zlsma=35, ce_mult=4)

            df_3.rename(columns={'signal':'signal_3'}, inplace=True)
            df_3.rename(columns={'sl':'sl_3'}, inplace=True)
            df_3.rename(columns={'tp_1':'tp_3_1'}, inplace=True)
            df_3.rename(columns={'tp_2':'tp_3_2'}, inplace=True)
            df_3.rename(columns={'tp_3':'tp_3_3'}, inplace=True)
            df_3.rename(columns={'tp_4':'tp_3_4'}, inplace=True)
            df_3.rename(columns={'tp_5':'tp_3_5'}, inplace=True)
            df_2.rename(columns={'signal':'signal_2'}, inplace=True)
            df_2.rename(columns={'sl':'sl_2'}, inplace=True)
            df_2.rename(columns={'tp_1':'tp_2_1'}, inplace=True)
            df_2.rename(columns={'tp_2':'tp_2_2'}, inplace=True)
            df_2.rename(columns={'tp_3':'tp_2_3'}, inplace=True)
            df_2.rename(columns={'tp_4':'tp_2_4'}, inplace=True)
            df_2.rename(columns={'tp_5':'tp_2_5'}, inplace=True)
            df_1.rename(columns={'signal':'signal_1'}, inplace=True)
            df_1.rename(columns={'sl':'sl_1'}, inplace=True)
            df_1.rename(columns={'tp_1':'tp_1_1'}, inplace=True)
            df_1.rename(columns={'tp_2':'tp_1_2'}, inplace=True)
            df_1.rename(columns={'tp_3':'tp_1_3'}, inplace=True)
            df_1.rename(columns={'tp_4':'tp_1_4'}, inplace=True)
            df_1.rename(columns={'tp_5':'tp_1_5'}, inplace=True)

            grosses_couilles = df_1.merge(df_2[['signal_2', 'sl_2', 'tp_2_1', 'tp_2_2', 'tp_2_3', 'tp_2_4', 'tp_2_5']], left_index=True, right_index=True, how='left') \
            .merge(df_3[['signal_3', 'sl_3', 'tp_3_1', 'tp_3_2', 'tp_3_3', 'tp_3_4', 'tp_3_5']], left_index=True, right_index=True, how='left') 
            
        elif symbol == 'GBPUSD':

            df_1 = DivergenceIchimoku(df_1, timeframe='M15', n_rsi=18, tolerance=3)
            df_2 = SuperTrends(df_2, timeframe='M15', ema=270, per_m5=14, per_m15=14, per_m30=18, atr_mul_m5=1, atr_mul_m15=2, atr_mul_m30=5)
            df_3 = ChandelierExitsZlsma(df_3, timeframe='M15', zlsma=10, ce_mult=2)

            df_3.rename(columns={'signal':'signal_3'}, inplace=True)
            df_3.rename(columns={'sl':'sl_3'}, inplace=True)
            df_3.rename(columns={'tp_1':'tp_3_1'}, inplace=True)
            df_3.rename(columns={'tp_2':'tp_3_2'}, inplace=True)
            df_3.rename(columns={'tp_3':'tp_3_3'}, inplace=True)
            df_3.rename(columns={'tp_4':'tp_3_4'}, inplace=True)
            df_3.rename(columns={'tp_5':'tp_3_5'}, inplace=True)
            df_2.rename(columns={'signal':'signal_2'}, inplace=True)
            df_2.rename(columns={'sl':'sl_2'}, inplace=True)
            df_2.rename(columns={'tp_1':'tp_2_1'}, inplace=True)
            df_2.rename(columns={'tp_2':'tp_2_2'}, inplace=True)
            df_2.rename(columns={'tp_3':'tp_2_3'}, inplace=True)
            df_2.rename(columns={'tp_4':'tp_2_4'}, inplace=True)
            df_2.rename(columns={'tp_5':'tp_2_5'}, inplace=True)
            df_1.rename(columns={'signal':'signal_1'}, inplace=True)
            df_1.rename(columns={'sl':'sl_1'}, inplace=True)
            df_1.rename(columns={'tp_1':'tp_1_1'}, inplace=True)
            df_1.rename(columns={'tp_2':'tp_1_2'}, inplace=True)
            df_1.rename(columns={'tp_3':'tp_1_3'}, inplace=True)
            df_1.rename(columns={'tp_4':'tp_1_4'}, inplace=True)
            df_1.rename(columns={'tp_5':'tp_1_5'}, inplace=True)

            grosses_couilles = df_1.merge(df_2[['signal_2', 'sl_2', 'tp_2_1', 'tp_2_2', 'tp_2_3', 'tp_2_4', 'tp_2_5']], left_index=True, right_index=True, how='left') \
            .merge(df_3[['signal_3', 'sl_3', 'tp_3_1', 'tp_3_2', 'tp_3_3', 'tp_3_4', 'tp_3_5']], left_index=True, right_index=True, how='left') \

    elif timeframe == 'M5':

        if symbol == 'EURUSD':

            df_2 = SuperTrends(df_2, timeframe='M5', ema=270, per_m5=10, per_m15=12, per_m30=16, atr_mul_m5=3, atr_mul_m15=5, atr_mul_m30=5)
            df_3 = ChandelierExitsZlsma(df_3, timeframe='M5', zlsma=35, ce_mult=2)
        
            df_2.rename(columns={'signal':'signal_2'}, inplace=True)
            df_2.rename(columns={'sl':'sl_2'}, inplace=True)
            df_2.rename(columns={'tp_1':'tp_2_1'}, inplace=True)
            df_2.rename(columns={'tp_2':'tp_2_2'}, inplace=True)
            df_2.rename(columns={'tp_3':'tp_2_3'}, inplace=True)
            df_2.rename(columns={'tp_4':'tp_2_4'}, inplace=True)
            df_2.rename(columns={'tp_5':'tp_2_5'}, inplace=True)
            df_3.rename(columns={'signal':'signal_3'}, inplace=True)
            df_3.rename(columns={'sl':'sl_3'}, inplace=True)
            df_3.rename(columns={'tp_1':'tp_3_1'}, inplace=True)
            df_3.rename(columns={'tp_2':'tp_3_2'}, inplace=True)
            df_3.rename(columns={'tp_3':'tp_3_3'}, inplace=True)
            df_3.rename(columns={'tp_4':'tp_3_4'}, inplace=True)
            df_3.rename(columns={'tp_5':'tp_3_5'}, inplace=True)

            grosses_couilles = df_2.merge(df_3[['signal_3', 'sl_3', 'tp_3_1', 'tp_3_2', 'tp_3_3', 'tp_3_4', 'tp_3_5']], left_index=True, right_index=True, how='left')\
                
        elif symbol == 'GBPUSD':

            df_2 = SuperTrends(df_2, timeframe='M5', ema=90, per_m5=13, per_m15=13, per_m30=18, atr_mul_m5=1, atr_mul_m15=2, atr_mul_m30=3)
            df_3 = ChandelierExitsZlsma(df_3, timeframe='M5', zlsma=30, ce_mult=4)
        
            df_2.rename(columns={'signal':'signal_2'}, inplace=True)
            df_2.rename(columns={'sl':'sl_2'}, inplace=True)
            df_2.rename(columns={'tp_1':'tp_2_1'}, inplace=True)
            df_2.rename(columns={'tp_2':'tp_2_2'}, inplace=True)
            df_2.rename(columns={'tp_3':'tp_2_3'}, inplace=True)
            df_2.rename(columns={'tp_4':'tp_2_4'}, inplace=True)
            df_2.rename(columns={'tp_5':'tp_2_5'}, inplace=True)
            df_3.rename(columns={'signal':'signal_3'}, inplace=True)
            df_3.rename(columns={'sl':'sl_3'}, inplace=True)
            df_3.rename(columns={'tp_1':'tp_3_1'}, inplace=True)
            df_3.rename(columns={'tp_2':'tp_3_2'}, inplace=True)
            df_3.rename(columns={'tp_3':'tp_3_3'}, inplace=True)
            df_3.rename(columns={'tp_4':'tp_3_4'}, inplace=True)
            df_3.rename(columns={'tp_5':'tp_3_5'}, inplace=True)

            grosses_couilles = df_2.merge(df_3[['signal_3', 'sl_3', 'tp_3_1', 'tp_3_2', 'tp_3_3', 'tp_3_4', 'tp_3_5']], left_index=True, right_index=True, how='left')\

    return grosses_couilles