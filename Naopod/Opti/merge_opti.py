from datetime import datetime, timedelta
from strategies_opti import *


def MergedDF(df_M30, df_M15, df_M5, extracted_params):
    
    current_time = datetime.now()
    seven_days_before = current_time - timedelta(days=31)

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

    ## Extract params

    # Define the keys you're interested in
    keys_of_interest = ['n_rsi_m15',
                        'n_rsi_m30',
                        'tol_m15',
                        'tol_m30',
                        'ema_m15',
                        'ema_m30',
                        'ema_m5',
                        'zlsma_m15',
                        'zlsma_m30',
                        'zlsma_m5',
                        'ce_mult_m15',
                        'ce_mult_m30',
                        'ce_mult_m5',
                        'per_1_m5',
                        'per_1_m15',
                        'per_1_m30', 
                        'atr_mul_1_m5',
                        'atr_mul_1_m15',
                        'atr_mul_1_m30',
                        'per_2_m5',
                        'per_2_m15',
                        'per_2_m30', 
                        'atr_mul_2_m5',
                        'atr_mul_2_m15',
                        'atr_mul_2_m30',
                        'per_3_m5',
                        'per_3_m15',
                        'per_3_m30', 
                        'atr_mul_3_m5',
                        'atr_mul_3_m15',
                        'atr_mul_3_m30']

    # Initialize a dictionary to store the extracted values
    extracted_values = {}

    # Iterate over the keys and populate the dictionary
    # Use dict.get() to provide a default value of 10 if the key is not found
    for key in keys_of_interest:
        extracted_values[key] = extracted_params.get(key, 10)

    ## Choose sl_tp type 
        # True : small
        # False : big

    sl_tp_val = False

    # Call strategies
    # 1
    df_1_M30 = DivergenceIchimoku(df_1_M30, timeframe='M30', 
                                  n_rsi=extracted_values['n_rsi_m30'], 
                                  tolerance=extracted_values['tol_m30'],
                                  small_sl_tp=sl_tp_val)
    df_1_M30 = df_1_M30[seven_days_before :]        
    df_1_M30.loc[(df_1_M30.index.hour < 9) | (df_1_M30.index.hour >= 20), 'signal'] = 0

    df_1_M15 = DivergenceIchimoku(df_1_M15, timeframe='M15', 
                                  n_rsi=extracted_values['n_rsi_m15'], 
                                  tolerance=extracted_values['tol_m15'],
                                  small_sl_tp=sl_tp_val)
    df_1_M15 = df_1_M15[seven_days_before :]
    df_1_M15.loc[(df_1_M15.index.hour < 9) | (df_1_M15.index.hour >= 20), 'signal'] = 0
        
    # 2
    df_2_M30 = SuperTrends(df_2_M30, 
                           timeframe='M30', 
                           ema=extracted_values['ema_m30'],
                           per_m5=extracted_values['per_1_m30'],
                           per_m15=extracted_values['per_2_m30'],
                           per_m30=extracted_values['per_3_m30'],
                           atr_mul_m5=extracted_values['atr_mul_1_m30'],
                           atr_mul_m15=extracted_values['atr_mul_2_m30'],
                           atr_mul_m30=extracted_values['atr_mul_3_m30'],
                           small_sl_tp=sl_tp_val)
    df_2_M30 = df_2_M30[seven_days_before :]
    df_2_M30.loc[(df_2_M30.index.hour < 9) | (df_2_M30.index.hour >= 20), 'signal'] = 0

    df_2_M15 = SuperTrends(df_2_M15, 
                           timeframe='M15', 
                           ema=extracted_values['ema_m15'],
                           per_m5=extracted_values['per_1_m15'],
                           per_m15=extracted_values['per_2_m15'],
                           per_m30=extracted_values['per_3_m15'],
                           atr_mul_m5=extracted_values['atr_mul_1_m15'],
                           atr_mul_m15=extracted_values['atr_mul_2_m15'],
                           atr_mul_m30=extracted_values['atr_mul_3_m15'],
                           small_sl_tp=sl_tp_val)
    df_2_M15 = df_2_M15[seven_days_before :]
    df_2_M15.loc[(df_2_M15.index.hour < 9) | (df_2_M15.index.hour >= 20), 'signal'] = 0

    df_2_M5 = SuperTrends(df_2_M5, 
                          timeframe='M5', 
                          ema=extracted_values['ema_m5'],
                          per_m5=extracted_values['per_1_m5'],
                           per_m15=extracted_values['per_2_m5'],
                           per_m30=extracted_values['per_3_m5'],
                           atr_mul_m5=extracted_values['atr_mul_1_m5'],
                           atr_mul_m15=extracted_values['atr_mul_2_m5'],
                           atr_mul_m30=extracted_values['atr_mul_3_m5'],
                           small_sl_tp=sl_tp_val)
    df_2_M5 = df_2_M5[seven_days_before :]
    df_2_M5.loc[(df_2_M5.index.hour < 9) | (df_2_M5.index.hour >= 20), 'signal'] = 0

    # 3
    df_3_M30 = ChandelierExitsZlsma(df_3_M30, 
                                    timeframe='M30', 
                                    zlsma=extracted_values['zlsma_m30'], 
                                    ce_mult=extracted_values['ce_mult_m30'],
                                    small_sl_tp=sl_tp_val
                                    )
    df_3_M30 = df_3_M30[seven_days_before :]
    df_3_M30.loc[(df_3_M30.index.hour < 9) | (df_3_M30.index.hour >= 20), 'signal'] = 0

    df_3_M15 = ChandelierExitsZlsma(df_3_M15, 
                                    timeframe='M15', 
                                    zlsma=extracted_values['zlsma_m15'], 
                                    ce_mult=extracted_values['ce_mult_m15'],
                                    small_sl_tp=sl_tp_val)
    df_3_M15 = df_3_M15[seven_days_before :]
    df_3_M15.loc[(df_3_M15.index.hour < 9) | (df_3_M15.index.hour >= 20), 'signal'] = 0

    df_3_M5 = ChandelierExitsZlsma(df_3_M5, 
                                   timeframe='M5', 
                                   zlsma=extracted_values['zlsma_m5'], 
                                   ce_mult=extracted_values['ce_mult_m5'],
                                   small_sl_tp=sl_tp_val)
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
