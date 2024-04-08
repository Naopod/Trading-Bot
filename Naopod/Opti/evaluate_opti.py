'''Produces statistics for the given combination'''

def evaluate_strategy(df, symbol):

    if symbol in ['EURUSD', 'GBPUSD', 'USDCAD', 'USDJPY', 'USDCHF']:
        volume = 100000
    else:
        volume = 0.5

    profits = [0] * len(df)
    active_trade = None

    for i in range(1, len(df)):
        new_signal = None
        current_entry = None
        new_sl = None
        new_tp = None
        current_hour = df.index[i].hour 
        
        # Check for signals from highest to lowest timeframe
        if df['final_signal_M30'].iloc[i] != 0:  # M30 signal
            current_entry = df['Close'].iloc[i-1]
            new_signal = df['final_signal_M30'].iloc[i]
            new_sl = df['final_sl_M30'].iloc[i]
            new_tp = df['final_tp_M30'].iloc[i]
        elif df['final_signal_M15'].iloc[i] != 0:  # M15 signal
            current_entry = df['Close'].iloc[i-1]
            new_signal = df['final_signal_M15'].iloc[i]
            new_sl = df['final_sl_M15'].iloc[i]
            new_tp = df['final_tp_M15'].iloc[i]
        elif df['final_signal_M5'].iloc[i] != 0:  # M5 signal
            current_entry = df['Close'].iloc[i-1]
            new_signal = df['final_signal_M5'].iloc[i]
            new_sl = df['final_sl_M5'].iloc[i]
            new_tp = df['final_tp_M5'].iloc[i]

        # Check for an opposite signal and close the active trade if present
        if active_trade is not None and new_signal is not None and active_trade["signal"] != new_signal:
            profit = volume * (df['Close'].iloc[i] - active_trade["entry"]) if active_trade["signal"] == 1 else volume * (active_trade["entry"] - df['Close'].iloc[i])
            profits[i] = profit
            active_trade = None

        # Check for new trade signal
        if new_signal is not None:
            active_trade = {
                "signal": new_signal,
                "entry": current_entry,
                "tp": new_tp,
                "sl": new_sl
            }

        # Check if active trade should be closed
        if active_trade is not None:
            closing_price = None

            if (active_trade["signal"] == 1 and df['High'].iloc[i] >= active_trade["tp"]) or \
               (active_trade["signal"] == -1 and df['Low'].iloc[i] <= active_trade["tp"]):
                closing_price = active_trade["tp"]
            elif (active_trade["signal"] == 1 and df['Low'].iloc[i] <= active_trade["sl"]) or \
                 (active_trade["signal"] == -1 and df['High'].iloc[i] >= active_trade["sl"]):
                closing_price = active_trade["sl"]
            
            if current_hour > 21:
                closing_price = df['Close'].iloc[i]

            if closing_price is not None:
                profit = volume * (closing_price - active_trade["entry"]) if active_trade["signal"] == 1 else volume * (active_trade["entry"] - closing_price)
                profits[i] = profit
                active_trade = None

    df['profit'] = profits

    return df   
