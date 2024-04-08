from Indicators import *
import pandas as pd

'''All the strategies'''

def DivergenceIchimoku(df,
                       timeframe : str, 
                       indicator : str = 'rsi', 
                       n_rsi: int=14, 
                       tolerance : int=3, 
                       small_sl_tp=True) -> pd.DataFrame:

    if indicator == 'rsi':
        df['rsi'] = RSI(df, n_rsi)
        df[['regularBull', 'regularBear', 'hiddenBull', 'hiddenBear']] = autodetect_divergence(df, df['rsi'], tolerance=tolerance)
    elif indicator == 'macd':
        df['rsi'] = RSI(df, n_rsi)
        df[['macd', 'hist', 'sign']] = MACD(df)
        df[['regularBull', 'regularBear', 'hiddenBull', 'hiddenBear']] = autodetect_divergence(df, df['macd'])
    elif indicator == 'stochrsi':
        df['rsi'] = RSI(df, n_rsi)
        df['K'], df['D'] = stoch_rsi(df, K_period=1)
        df[['regularBull', 'regularBear', 'hiddenBull', 'hiddenBear']] = autodetect_divergence(df, df['K'])
    df['ema']=EMA(df, 200)
    df = ichimoku_cloud(df)
    df['atr']=ATR(df)
    signal = [0] * len(df)
    sl=[0]*len(df)
    tp=[0]*len(df)

    '''
    Pour chaque timeframe, on peut modifier le stop loss et le take profit. On peut aussi faire la différence entre les trades BUY ou SELL. Le stop loss d'un trade
    BUY est 'sl_long', celui d'un trade SELL est 'sl_short'. Pareil pour le take profit, le take profit d'un trade achat est 'tp_long' et celui d'un trade SELL
    est 'tp_short'. '''

    if not small_sl_tp: 

        if timeframe == 'M15':
            df['sl_long'] = df.Low.rolling(2).min() - df.atr/4
            df['sl_short'] = df.High.rolling(2).max() + df.atr/4
            df['tp_long'] = df.Close + 1.4*(df.Close - (df.Low.rolling(2).min() - df.atr/4)) 
            df['tp_short'] = df.Close - 1.4*((df.High.rolling(2).max() + df.atr/4) - df.Close)
        else:
            df['sl_long'] = df.Low.rolling(2).min() - df.atr/4
            df['sl_short'] = df.High.rolling(2).max() + df.atr/4
            df['tp_long'] = df.Close + 1.3*(df.Close - (df.Low.rolling(2).min() - df.atr/4)) 
            df['tp_short'] = df.Close - 1.3*((df.High.rolling(2).max() + df.atr/4) - df.Close)
    
    elif small_sl_tp:

        if timeframe == 'M15':
            df['sl_long'] = df.Low.rolling(2).min() - df.atr/5.25
            df['sl_short'] = df.High.rolling(2).max() + df.atr/5.25
            df['tp_long'] = df.Close + 0.15*(df.Close - (df.Low.rolling(2).min() - df.atr/3.25)) 
            df['tp_short'] = df.Close - 0.2*((df.High.rolling(2).max() + df.atr/3.25) - df.Close)
        else:
            df['sl_long'] = df.Low.rolling(2).min() - df.atr/6
            df['sl_short'] = df.High.rolling(2).max() + df.atr/5.85
            df['tp_long'] = df.Close + 0.15*(df.Close - (df.Low.rolling(2).min() - df.atr/4)) 
            df['tp_short'] = df.Close - 0.2*((df.High.rolling(2).max() + df.atr/3.85) - df.Close)

    for i in range(len(df)):
        if df['regularBull'][i] == 1 and df['hiddenBull'][i] == 1 and df['regularBear'][i] == 0 and df['hiddenBear'][i] == 0 and df['ema'][i] < df['above_cloud'][i] and df.fdi.iloc[i]<1.5:
            signal[i] = 1 
            sl[i] = df.sl_long.iloc[i]
            tp[i] = df.tp_long.iloc[i]
        elif df['regularBull'][i] == 1 and df['hiddenBull'][i] == 0 and df['regularBear'][i] == 0 and df['hiddenBear'][i] == 0 and df['ema'][i] < df['above_cloud'][i] and df.fdi.iloc[i]<1.5: 
            signal[i] = 1 
            sl[i] = df.sl_long.iloc[i]
            tp[i] = df.tp_long.iloc[i]
        elif df['regularBull'][i] == 0 and df['hiddenBull'][i] == 1 and df['regularBear'][i] == 0 and df['hiddenBear'][i] == 0 and df['ema'][i] < df['above_cloud'][i] and df.fdi.iloc[i]<1.5:
            signal[i] = 1 
            sl[i] = df.sl_long.iloc[i]
            tp[i] = df.tp_long.iloc[i]
        elif df['regularBull'][i] == 0 and df['hiddenBull'][i] == 0 and df['regularBear'][i] == 1 and df['hiddenBear'][i] == 1 and df['ema'][i] > df['below_cloud'][i] and df.fdi.iloc[i]<1.5:
            signal[i] = -1
            sl[i] = df.sl_short.iloc[i]
            tp[i] = df.tp_short.iloc[i]
        elif df['regularBull'][i] == 0 and df['hiddenBull'][i] == 0 and df['regularBear'][i] == 1 and df['hiddenBear'][i] == 0 and df['ema'][i] > df['below_cloud'][i] and df.fdi.iloc[i]<1.5:
            signal[i] = -1
            sl[i] = df.sl_short.iloc[i]
            tp[i] = df.tp_short.iloc[i]
        elif df['regularBull'][i] == 0 and df['hiddenBull'][i] == 0 and df['regularBear'][i] == 0 and df['hiddenBear'][i] == 1 and df['ema'][i] > df['below_cloud'][i] and df.fdi.iloc[i]<1.5:
            signal[i] = -1 
            sl[i] = df.sl_short.iloc[i]
            tp[i] = df.tp_short.iloc[i]
        else:
            signal[i] = 0

    df['signal'] = signal
    df['sl']=sl
    df['tp']=tp
    
    return df

''' STRAT 2'''

def SuperTrends(df,
                timeframe: str, 
                ema: int=200,
                per_m5: int=10,
                per_m15: int=11,
                per_m30: int=12,
                atr_mul_m5: int=1,
                atr_mul_m15: int=2,
                atr_mul_m30: int=3,
                small_sl_tp=True)->pd.DataFrame:
    

    df['rsi'] = RSI(df)
    df[['uptrend_1', 'downtrend_1', 'trend_1']] = supertrend(df, period=per_m5, ATR_multiplier=atr_mul_m5)
    df[['uptrend_2', 'downtrend_2', 'trend_2']] = supertrend(df, period=per_m15, ATR_multiplier=atr_mul_m15)
    df[['uptrend_3', 'downtrend_3', 'trend_3']] = supertrend(df, period=per_m30, ATR_multiplier=atr_mul_m30)
    df['ema'] = EMA(df, ema)
    df['atr']=ATR(df)
    position_slow =[0]*len(df)
    position_mid =[0]*len(df)
    signal =[0]*len(df)
    sl=[0]*len(df)
    tp=[0]*len(df)

    '''
    Pour chaque timeframe, on peut modifier le stop loss et le take profit. On peut aussi faire la différence entre les trades BUY ou SELL. Le stop loss d'un trade
    BUY est 'sl_long', celui d'un trade SELL est 'sl_short'. Pareil pour le take profit, le take profit d'un trade achat est 'tp_long' et celui d'un trade SELL
    est 'tp_short'.
    
    '''

    if not small_sl_tp: 

        if timeframe == 'M5':
            df['sl_long'] = df.trend_2 - df.atr/4
            df['sl_short'] = df.trend_2 + df.atr/4
            df['tp_long'] = df.Close + 1.5*(df.Close - (df.trend_2 - df.atr/4)) 
            df['tp_short'] = df.Close - 1.5*((df.trend_2 + df.atr/4) - df.Close)
        elif timeframe == 'M15':
            df['sl_long'] = df.trend_2 - df.atr/4
            df['sl_short'] = df.trend_2 + df.atr/4
            df['tp_long'] = df.Close + 1.4*(df.Close - (df.trend_2 - df.atr/4)) 
            df['tp_short'] = df.Close - 1.4*((df.trend_2 + df.atr/4) - df.Close)
        else:
            df['sl_long'] = df.trend_2 - df.atr/4
            df['sl_short'] = df.trend_2 + df.atr/4
            df['tp_long'] = df.Close + 1.3*(df.Close - (df.trend_2 - df.atr/4)) 
            df['tp_short'] = df.Close - 1.3*((df.trend_2 + df.atr/4) - df.Close)
    
    elif small_sl_tp:

        if timeframe == 'M5':
            df['sl_long'] = df.trend_2 - df.atr/4
            df['sl_short'] = df.trend_2 + df.atr/4
            df['tp_long'] = df.Close + 0.25*(df.Close - (df.trend_2 - df.atr/4)) 
            df['tp_short'] = df.Close - 0.3*((df.trend_2 + df.atr/4) - df.Close)
        elif timeframe == 'M15':
            df['sl_long'] = df.trend_2 - df.atr/4
            df['sl_short'] = df.trend_2 + df.atr/4
            df['tp_long'] = df.Close + 0.15*(df.Close - (df.trend_2 - df.atr/4)) 
            df['tp_short'] = df.Close - 0.2*((df.trend_2 + df.atr/4) - df.Close)
        else:
            df['sl_long'] = df.trend_2 - df.atr/4
            df['sl_short'] = df.trend_2 + df.atr/4
            df['tp_long'] = df.Close + 0.15*(df.Close - (df.trend_2 - df.atr/4)) 
            df['tp_short'] = df.Close - 0.2*((df.trend_2 + df.atr/4) - df.Close)

    for i in range(len(df)):
        if df.trend_1.iloc[i-1] == 1 and df.trend_1.iloc[i] == -1:
            position_slow[i] = -1
        elif df.trend_1.iloc[i-1] == -1 and df.trend_1.iloc[i] == 1:
            position_slow[i] = 1
        else:
            position_slow[i] = 0

    df['position_slow']=position_slow

    for i in range(len(df)):
        if df.position_slow.iloc[i-1] == 1 and df.position_slow.iloc[i] == 0:
            df.position_slow.iloc[i] = 1
        elif df.position_slow.iloc[i-1] == -1 and df.position_slow.iloc[i] == 0:
            df.position_slow.iloc[i] = -1
        elif df.position_slow.iloc[i-1] == 1 and df.position_slow.iloc[i] == -1:
            df.position_slow.iloc[i] == -1
        elif df.position_slow.iloc[i] == -1 and df.position_slow.iloc[i] == 1:
            df.position_slow.iloc[i] = 1
    for i in range(len(df)):
        if df.trend_2.iloc[i-1] == 1 and df.trend_2.iloc[i] == -1 and df.position_slow.iloc[i] == -1:
            position_mid[i] = -1
        elif df.trend_2.iloc[i-1] == -1 and df.trend_2.iloc[i] == 1 and df.position_slow.iloc[i] == 1:
            position_mid[i] = 1

    df['position_mid']=position_mid

    for i in range(len(df)):
        if df.position_mid.iloc[i-1] == 1 and df.position_mid.iloc[i] == 0:
            df.position_mid.iloc[i] = 1
        elif df.position_mid.iloc[i-1] == -1 and df.position_mid.iloc[i] == 0:
            df.position_mid.iloc[i] = -1
        elif df.position_mid.iloc[i-1] == 1 and df.position_mid.iloc[i] == -1:
            df.position_mid.iloc[i] == -1
        elif df.position_mid.iloc[i] == -1 and df.position_mid.iloc[i] == 1:
            df.position_mid.iloc[i] = 1    
    for i in range(len(df)):
        if df.trend_3.iloc[i-1] == 1 and df.trend_3.iloc[i] == -1 and df.position_mid.iloc[i] == -1 and df.ema.iloc[i] > df.Close.iloc[i] and df.fdi.iloc[i]<1.5:
            signal[i] = -1
            sl[i] = df.sl_short.iloc[i]
            tp[i] = df.tp_short.iloc[i]
        elif df.trend_3.iloc[i-1] == -1 and df.trend_3.iloc[i] == 1 and df.position_mid.iloc[i] == 1 and df.ema.iloc[i] < df.Close.iloc[i] and df.fdi.iloc[i]<1.5:
            signal[i] = 1
            sl[i] = df.sl_long.iloc[i]
            tp[i] = df.tp_long.iloc[i]

    df['signal']=signal
    df['sl']=sl
    df['tp']=tp

    return df

''' STRAT 6 '''

def ChandelierExitsZlsma(df, 
                         timeframe: str, 
                         zlsma: int=20, 
                         ce_mult: int=2,
                         small_sl_tp=True)->pd.DataFrame:    

    df[['longstop', 'shortstop', 'direction', 'signals']] = chandelier_exit(df, mult=ce_mult)
    df['rsi'] = RSI(df)
    df['zlsma'] = ZLSMA(df, zlsma)
    df['atr']=ATR(df)
    signal = [0]*len(df)
    tp=[0]*len(df)
    sl=[0]*len(df)

    '''

    Pour chaque timeframe, on peut modifier le stop loss et le take profit. On peut aussi faire la différence entre les trades BUY ou SELL. Le stop loss d'un trade
    BUY est 'sl_long', celui d'un trade SELL est 'sl_short'. Pareil pour le take profit, le take profit d'un trade achat est 'tp_long' et celui d'un trade SELL
    est 'tp_short'.

    '''

    
    if not small_sl_tp: 

        if timeframe == 'M5':
            df['sl_long'] = df.Low.rolling(2).min() - df.atr/4
            df['sl_short'] = df.High.rolling(2).max() + df.atr/4
            df['tp_long'] = df.Close + 1.5*(df.Close - (df.Low.rolling(2).min() - df.atr/4)) 
            df['tp_short'] = df.Close - 1.5*((df.High.rolling(2).max() + df.atr/4) - df.Close)
        elif timeframe == 'M15':
            df['sl_long'] = df.Low.rolling(2).min() - df.atr/4
            df['sl_short'] = df.High.rolling(2).max() + df.atr/4
            df['tp_long'] = df.Close + 1.4*(df.Close - (df.Low.rolling(2).min() - df.atr/4)) 
            df['tp_short'] = df.Close - 1.4*((df.High.rolling(2).max() + df.atr/4) - df.Close)
        else:
            df['sl_long'] = df.Low.rolling(2).min() - df.atr/4
            df['sl_short'] = df.High.rolling(2).max() + df.atr/4
            df['tp_long'] = df.Close + 1.3*(df.Close - (df.Low.rolling(2).min() - df.atr/4)) 
            df['tp_short'] = df.Close - 1.3*((df.High.rolling(2).max() + df.atr/4) - df.Close)
    
    elif small_sl_tp:

        if timeframe == 'M5':
            df['sl_long'] = df.Low.rolling(2).min() - df.atr/5
            df['sl_short'] = df.High.rolling(2).max() + df.atr/5
            df['tp_long'] = df.Close + 0.25*(df.Close - (df.Low.rolling(2).min() - df.atr/3)) 
            df['tp_short'] = df.Close - 0.3*((df.High.rolling(2).max() + df.atr/3) - df.Close)
        elif timeframe == 'M15':
            df['sl_long'] = df.Low.rolling(2).min() - df.atr/5.25
            df['sl_short'] = df.High.rolling(2).max() + df.atr/5.25
            df['tp_long'] = df.Close + 0.15*(df.Close - (df.Low.rolling(2).min() - df.atr/3.25)) 
            df['tp_short'] = df.Close - 0.2*((df.High.rolling(2).max() + df.atr/3.25) - df.Close)
        else:
            df['sl_long'] = df.Low.rolling(2).min() - df.atr/6
            df['sl_short'] = df.High.rolling(2).max() + df.atr/5.85
            df['tp_long'] = df.Close + 0.15*(df.Close - (df.Low.rolling(2).min() - df.atr/4)) 
            df['tp_short'] = df.Close - 0.2*((df.High.rolling(2).max() + df.atr/3.85) - df.Close)

    for i in range(len(df)):
        if df.signals.iloc[i] == 1 and crossover(df['Close'], df['zlsma']).iloc[i] == 1 and df.fdi.iloc[i]<1.5:
            signal[i] = 1
            sl[i] = df.sl_long.iloc[i]
            tp[i] = df.tp_long.iloc[i]
        elif df.signals.iloc[i] == -1 and crossover(df['zlsma'], df['Close']).iloc[i] == 1 and df.fdi.iloc[i]<1.5:
            signal[i] = -1
            sl[i] = df.sl_short.iloc[i]
            tp[i] = df.tp_short.iloc[i]

    df['signal']=signal
    df['sl']=sl
    df['tp']=tp

    return df

