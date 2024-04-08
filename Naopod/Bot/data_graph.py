import MetaTrader5 as mt
import pandas as pd
from Indicators import FDI
from datetime import datetime, timedelta
from strategies_graph import DivergenceIchimoku, SuperTrends, ChandelierExitsZlsma


'''Data for the graph'''

def GetData(symbol):
    mt.initialize()

    # Extract data we want to work on, using different timeframes
    df_M30 = pd.DataFrame(mt.copy_rates_from_pos(symbol, mt.TIMEFRAME_M30, 1, 800))
    df_M15 = pd.DataFrame(mt.copy_rates_from_pos(symbol, mt.TIMEFRAME_M15, 1, 1000))
    df_M5 = pd.DataFrame(mt.copy_rates_from_pos(symbol, mt.TIMEFRAME_M5, 1, 2200))

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


def MergedDF(symbol):
    current_time = datetime.now()
    seven_days_before = current_time - timedelta(days=9)

    # Create copies for the strategies
    df_M30, df_M15, df_M5 = GetData(symbol)

    # M30 copies
    df_1_M30 = df_M30.copy()
    df_2_M30 = df_M30.copy()
    df_3_M30 = df_M30.copy()

    # M15 copies
    df_2_M15 = df_M15.copy()
    df_1_M15 = df_M15.copy()
    df_3_M15 = df_M15.copy()

    # M5 copies
    df_2_M5 = df_M5.copy()
    df_3_M5 = df_M5.copy()

    # Call strategies

    sl_tp_val = True

    # 1
    if symbol == 'EURUSD':
        df_1_M30 = DivergenceIchimoku(df_1_M30, timeframe='M30', n_rsi=24, tolerance=6, small_sl_tp=sl_tp_val)
        df_1_M30 = df_1_M30[seven_days_before :]
        df_1_M30.loc[(df_1_M30.index.hour < 9) | (df_1_M30.index.hour >= 20), 'signal'] = 0

        df_1_M15 = DivergenceIchimoku(df_1_M15, timeframe='M15', n_rsi=18, tolerance=1, small_sl_tp=sl_tp_val)
        df_1_M15 = df_1_M15[seven_days_before :]
        df_1_M15.loc[(df_1_M15.index.hour < 9) | (df_1_M15.index.hour >= 20), 'signal'] = 0
        
        # 2
        df_2_M30 = SuperTrends(df_2_M30, timeframe='M30', ema=160, per_m5=14, per_m15=14, per_m30=17, atr_mul_m5=2, atr_mul_m15=4, atr_mul_m30=5, small_sl_tp=sl_tp_val)
        df_2_M30 = df_2_M30[seven_days_before :]
        df_2_M30.loc[(df_2_M30.index.hour < 9) | (df_2_M30.index.hour >= 20), 'signal'] = 0

        df_2_M15 = SuperTrends(df_2_M15, timeframe='M15', ema=230, per_m5=10, per_m15=13, per_m30=17, atr_mul_m5=1, atr_mul_m15=5, atr_mul_m30=5, small_sl_tp=sl_tp_val)
        df_2_M15 = df_2_M15[seven_days_before :]
        df_2_M15.loc[(df_2_M15.index.hour < 9) | (df_2_M15.index.hour >= 20), 'signal'] = 0

        df_2_M5 = SuperTrends(df_2_M5, timeframe='M5', ema=270, per_m5=10, per_m15=12, per_m30=16, atr_mul_m5=3, atr_mul_m15=5, atr_mul_m30=5, small_sl_tp=sl_tp_val)
        df_2_M5 = df_2_M5[seven_days_before :]
        df_2_M5.loc[(df_2_M5.index.hour < 9) | (df_2_M5.index.hour >= 20), 'signal'] = 0

        # 3
        df_3_M30 = ChandelierExitsZlsma(df_3_M30, timeframe='M30', zlsma=25, ce_mult=4, small_sl_tp=sl_tp_val)
        df_3_M30 = df_3_M30[seven_days_before :]
        df_3_M30.loc[(df_3_M30.index.hour < 9) | (df_3_M30.index.hour >= 20), 'signal'] = 0

        df_3_M15 = ChandelierExitsZlsma(df_3_M15, timeframe='M15', zlsma=35, ce_mult=4, small_sl_tp=sl_tp_val)
        df_3_M15 = df_3_M15[seven_days_before :]
        df_3_M15.loc[(df_3_M15.index.hour < 9) | (df_3_M15.index.hour >= 20), 'signal'] = 0

        df_3_M5 = ChandelierExitsZlsma(df_3_M5, timeframe='M5', zlsma=35, ce_mult=2, small_sl_tp=sl_tp_val)
        df_3_M5 = df_3_M5[seven_days_before :]
        df_3_M5.loc[(df_3_M5.index.hour < 9) | (df_3_M5.index.hour >= 20), 'signal'] = 0

    elif symbol == 'GBPUSD':
        df_1_M30 = DivergenceIchimoku(df_1_M30, timeframe='M30', n_rsi=14, tolerance=5, small_sl_tp=sl_tp_val)
        df_1_M30 = df_1_M30[seven_days_before :]
        df_1_M30.loc[(df_1_M30.index.hour < 9) | (df_1_M30.index.hour >= 20), 'signal'] = 0

        df_1_M15 = DivergenceIchimoku(df_1_M15, timeframe='M15', n_rsi=18, tolerance=3, small_sl_tp=sl_tp_val)
        df_1_M15 = df_1_M15[seven_days_before :]
        df_1_M15.loc[(df_1_M15.index.hour < 9) | (df_1_M15.index.hour >= 20), 'signal'] = 0
        
        # 2
        df_2_M30 = SuperTrends(df_2_M30, timeframe='M30', ema=270, per_m5=11, per_m15=12, per_m30=16, atr_mul_m5=2, atr_mul_m15=4, atr_mul_m30=5, small_sl_tp=sl_tp_val)
        df_2_M30 = df_2_M30[seven_days_before :]
        df_2_M30.loc[(df_2_M30.index.hour < 9) | (df_2_M30.index.hour >= 20), 'signal'] = 0

        df_2_M15 = SuperTrends(df_2_M15, timeframe='M15', ema=270, per_m5=14, per_m15=14, per_m30=18, atr_mul_m5=1, atr_mul_m15=2, atr_mul_m30=5, small_sl_tp=sl_tp_val)
        df_2_M15 = df_2_M15[seven_days_before :]
        df_2_M15.loc[(df_2_M15.index.hour < 9) | (df_2_M15.index.hour >= 20), 'signal'] = 0

        df_2_M5 = SuperTrends(df_2_M5, timeframe='M5', ema=90, per_m5=13, per_m15=13, per_m30=18, atr_mul_m5=1, atr_mul_m15=2, atr_mul_m30=3, small_sl_tp=sl_tp_val)
        df_2_M5 = df_2_M5[seven_days_before :]
        df_2_M5.loc[(df_2_M5.index.hour < 9) | (df_2_M5.index.hour >= 20), 'signal'] = 0

        # 3
        df_3_M30 = ChandelierExitsZlsma(df_3_M30, timeframe='M30', zlsma=25, ce_mult=3, small_sl_tp=sl_tp_val)
        df_3_M30 = df_3_M30[seven_days_before :]
        df_3_M30.loc[(df_3_M30.index.hour < 9) | (df_3_M30.index.hour >= 20), 'signal'] = 0

        df_3_M15 = ChandelierExitsZlsma(df_3_M15, timeframe='M15', zlsma=10, ce_mult=2, small_sl_tp=sl_tp_val)
        df_3_M15 = df_3_M15[seven_days_before :]
        df_3_M15.loc[(df_3_M15.index.hour < 9) | (df_3_M15.index.hour >= 20), 'signal'] = 0

        df_3_M5 = ChandelierExitsZlsma(df_3_M5, timeframe='M5', zlsma=30, ce_mult=4, small_sl_tp=sl_tp_val)
        df_3_M5 = df_3_M5[seven_days_before :]
        df_3_M5.loc[(df_3_M5.index.hour < 9) | (df_3_M5.index.hour >= 20), 'signal'] = 0

    # Merge everything
    df_3_M30.rename(columns={'signal': 'signal_M30_3'}, inplace=True)
    df_3_M15.rename(columns={'signal': 'signal_M15_3'}, inplace=True)
    df_3_M30.rename(columns={'sl': 'sl_M30_3'}, inplace=True)
    df_3_M15.rename(columns={'sl': 'sl_M15_3'}, inplace=True)
    df_3_M30.rename(columns={'tp': 'tp_M30_3'}, inplace=True)
    df_3_M15.rename(columns={'tp': 'tp_M15_3'}, inplace=True)
    df_3_M5.rename(columns={'tp': 'tp_M5_3'}, inplace=True)
    df_3_M5.rename(columns={'sl': 'sl_M5_3'}, inplace=True)
    df_3_M5.rename(columns={'signal': 'signal_M5_3'}, inplace=True)

    df_2_M30.rename(columns={'signal': 'signal_M30_2'}, inplace=True)
    df_2_M15.rename(columns={'signal': 'signal_M15_2'}, inplace=True)
    df_2_M5.rename(columns={'signal': 'signal_M5_2'}, inplace=True)
    df_2_M30.rename(columns={'sl': 'sl_M30_2'}, inplace=True)
    df_2_M15.rename(columns={'sl': 'sl_M15_2'}, inplace=True)
    df_2_M5.rename(columns={'sl': 'sl_M5_2'}, inplace=True)
    df_2_M30.rename(columns={'tp': 'tp_M30_2'}, inplace=True)
    df_2_M15.rename(columns={'tp': 'tp_M15_2'}, inplace=True)
    df_2_M5.rename(columns={'tp': 'tp_M5_2'}, inplace=True)

    df_1_M15.rename(columns={'signal': 'signal_M15_1'}, inplace=True)
    df_1_M30.rename(columns={'signal': 'signal_M30_1'}, inplace=True)
    df_1_M30.rename(columns={'sl': 'sl_M30_1'}, inplace=True)
    df_1_M15.rename(columns={'sl': 'sl_M15_1'}, inplace=True)
    df_1_M30.rename(columns={'tp': 'tp_M30_1'}, inplace=True)
    df_1_M15.rename(columns={'tp': 'tp_M15_1'}, inplace=True)

    # Shift M5 parameters by 1
    df_3_M5['signal_M5_3'] = df_3_M5['signal_M5_3'].shift(1)
    df_3_M5['sl_M5_3'] = df_3_M5['sl_M5_3'].shift(1)
    df_3_M5['tp_M5_3'] = df_3_M5['tp_M5_3'].shift(1)

    df_2_M5['signal_M5_2'] = df_2_M5['signal_M5_2'].shift(1)
    df_2_M5['sl_M5_2'] = df_2_M5['sl_M5_2'].shift(1)
    df_2_M5['tp_M5_2'] = df_2_M5['tp_M5_2'].shift(1)

    # Shift M15 parameters by 1
    df_3_M15['signal_M15_3'] = df_3_M15['signal_M15_3'].shift(1)
    df_3_M15['sl_M15_3'] = df_3_M15['sl_M15_3'].shift(1)
    df_3_M15['tp_M15_3'] = df_3_M15['tp_M15_3'].shift(1)

    df_2_M15['signal_M15_2'] = df_2_M15['signal_M15_2'].shift(1)
    df_2_M15['sl_M15_2'] = df_2_M15['sl_M15_2'].shift(1)
    df_2_M15['tp_M15_2'] = df_2_M15['tp_M15_2'].shift(1)

    df_1_M15['signal_M15_1'] = df_1_M15['signal_M15_1'].shift(1)
    df_1_M15['sl_M15_1'] = df_1_M15['sl_M15_1'].shift(1)
    df_1_M15['tp_M15_1'] = df_1_M15['tp_M15_1'].shift(1)

    # Shift M30 parameters by 1
    df_3_M30['signal_M30_3'] = df_3_M30['signal_M30_3'].shift(1)
    df_3_M30['sl_M30_3'] = df_3_M30['sl_M30_3'].shift(1)
    df_3_M30['tp_M30_3'] = df_3_M30['tp_M30_3'].shift(1)

    df_2_M30['signal_M30_2'] = df_2_M30['signal_M30_2'].shift(1)
    df_2_M30['sl_M30_2'] = df_2_M30['sl_M30_2'].shift(1)
    df_2_M30['tp_M30_2'] = df_2_M30['tp_M30_2'].shift(1)

    df_1_M30['signal_M30_1'] = df_1_M30['signal_M30_1'].shift(1)
    df_1_M30['sl_M30_1'] = df_1_M30['sl_M30_1'].shift(1)
    df_1_M30['tp_M30_1'] = df_1_M30['tp_M30_1'].shift(1)


    merged_df = df_2_M5.merge(df_3_M30[['signal_M30_3', 'sl_M30_3', 'tp_M30_3']], left_index=True, right_index=True, how='left') \
        .merge(df_3_M15[['signal_M15_3', 'sl_M15_3', 'tp_M15_3']], left_index=True, right_index=True, how='left') \
        .merge(df_3_M5[['signal_M5_3', 'sl_M5_3', 'tp_M5_3']], left_index=True, right_index=True, how='left') \
        .merge(df_2_M30[['signal_M30_2', 'sl_M30_2', 'tp_M30_2']], left_index=True, right_index=True, how='left') \
        .merge(df_2_M15[['signal_M15_2', 'sl_M15_2', 'tp_M15_2']], left_index=True, right_index=True, how='left') \
        .merge(df_1_M15[['signal_M15_1', 'sl_M15_1', 'tp_M15_1']], left_index=True, right_index=True, how='left') \
        .merge(df_1_M30[['signal_M30_1', 'sl_M30_1', 'tp_M30_1']], left_index=True, right_index=True, how='left') \
        .fillna(0)

    return merged_df

