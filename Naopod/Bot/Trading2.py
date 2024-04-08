import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import time
from Minette import Porte
from Indicators import ATR
import math
import numpy as np
from Graph import Plot
import PySimpleGUI as sg
import json
import os
from threading import Thread
import webbrowser
from twilio.rest import Client 
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template_string
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class CantSleep:

    def __init__(self):
        
        if mt5.initialize():
            print('Connected to MetaTrader5')
            print('Login: ', mt5.account_info().login)
            print('Server: ', mt5.account_info().server)
        elif not mt5.initialize():
            print('Failed to connect to the account')

    def __del__(self):

        mt5.shutdown()
        print('Disconnected from MetaTrader 5')

    def market_order(self, SYMBOL, VOLUME, order_type, stoploss, deviation=20, magic=12345):

        order_type_dict = {
            'buy': mt5.ORDER_TYPE_BUY,
            'sell': mt5.ORDER_TYPE_SELL
        }

        price_dict = {
            'buy': mt5.symbol_info_tick(SYMBOL).ask,
            'sell': mt5.symbol_info_tick(SYMBOL).bid
        }

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": SYMBOL,
            "volume": VOLUME,  # FLOAT
            "type": order_type_dict[order_type],
            "price": price_dict[order_type],
            "sl": stoploss,  # FLOAT
            "deviation": deviation,  # INTERGER
            "magic": magic,  # INTERGER
            "comment": 'scalp_open',
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        order_result = mt5.order_send(request)
        return(order_result)

    def close_position(self, symbol, position, volume, deviation=20, magic=12345):

        order_type_dict = {
            0: mt5.ORDER_TYPE_SELL,
            1: mt5.ORDER_TYPE_BUY
        }

        price_dict = {
            0: mt5.symbol_info_tick(symbol).bid,
            1: mt5.symbol_info_tick(symbol).ask
        }

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": position['ticket'],  # select the position you want to close
            "symbol": symbol,
            "volume": volume,  # FLOAT
            "type": order_type_dict[position['type']],
            "price": price_dict[position['type']],
            "deviation": deviation,  # INTERGER
            "magic": magic,  # INTERGER
            "comment": 'scalp_close',
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        order_result = mt5.order_send(request)
        return(order_result)

    def close_positions(self, order_type, symbol):
        order_type_dict = {
            'buy': 0,
            'sell': 1
        }

        if len(mt5.positions_get()) > 0:
            o_pos = mt5.positions_get()
            df_pos = pd.DataFrame (list(o_pos), columns=o_pos[0]._asdict().keys())
            matching_symbols = df_pos[df_pos['symbol'] == symbol].shape[0]
            if matching_symbols > 0:
                
                filtered_df = df_pos[df_pos['symbol'] == symbol]
                volume = filtered_df['volume'].sum()
                positions_df = pd.DataFrame (list(o_pos), columns=o_pos[0]._asdict().keys())

                if order_type != 'all':
                    positions_df = positions_df[(positions_df['type'] == order_type_dict[order_type]) & (positions_df['symbol'] == symbol)]

                for i, position in positions_df.iterrows():
                    order_result = self.close_position(symbol, position, volume)

                return order_result

    def get_exposure(self, symbol):
        positions = mt5.positions_get(symbol=symbol)
        if positions:
            pos_df = pd.DataFrame(positions, columns=positions[0]._asdict().keys())
            exposure = pos_df['volume'].sum()

            return exposure
    
    def get_all_positions(self):
            
            try:
                #mt5.initialize( login = name, server = serv, password = key, path = path)
                o_pos = mt5.positions_get()
                df_pos = pd.DataFrame (list(o_pos), columns=o_pos[0]._asdict().keys())
                    
            except :
                df_pos = pd.DataFrame()

            return df_pos
    
    def get_volume(self, symbol):

        start = 0.01
        end = 100.0
        step = 0.01

        numbers = np.arange(start, end + step, step)

        values_base = {round(num, 2): round(num, 2) * 100000 for num in numbers}

        account_info = mt5.account_info()
        balance = account_info.equity

        cash = int(balance)
        leverage_cash = cash * 500
        leverage_cash_rounded = math.floor(leverage_cash / 100) * 100
        volume_in_cash = leverage_cash_rounded * 0.3

        min_difference = float('inf')

        for num, value in values_base.items():
            difference = abs(value - volume_in_cash)
            if difference < min_difference:
                min_difference = difference
                VOLUME = num

        if symbol in ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCAD', 'USDCHF']:
            VOLUME = 0.7
        elif symbol in ['GOLD', 'SILVER']:
            VOLUME = 0.2

        return float(VOLUME)

def check_allowed_trading_hours(symbol):
    '''Add market specifications'''
    if 9 < datetime.now().hour < 24 and datetime.now().weekday() not in (5,6):
        return True
    else:
        return False
    
def send_sms(msg):
    "Y4_X__gSZQFCiSFh2Fx46QRvF1TqZ96-oiHjF5oM"
    account_sid='AC4667dbe3c5008a364a8dc5faa59f853f'
    auth_token='111ed5c108832943461aec8e93cf0312'
    client=Client(account_sid, auth_token)

    client.messages.create(
        body=msg,
        from_='+16815400090',
        to='+330679001733'
    )

def fetch_news():

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}

    u = 'https://www.forexfactory.com/market/'

    session = requests.Session()
    r = session.get(u, timeout=30, headers=headers)

    soup = BeautifulSoup(r.content, 'html.parser')

    news_high = []

    # High impacts
    for news_item in soup.select('.flexposts__item.flexposts__story.flexposts__story--high'):
        time = news_item.select_one('.flexposts__nowrap.flexposts__time').text if news_item.select_one('.flexposts__nowrap.flexposts__time') else '' 
        title = news_item.select_one('.flexposts__story-title').text if news_item.select_one('.flexposts__story-title') else ''  
        impact = 'high'
        
        # Find the 'a' tag with the specific class attributes within this news_item
        a_tag = news_item.find('a', {'href': True})
        
        # Extract the 'title' attribute from the 'a' tag if it exists
        href = a_tag.get('href') if a_tag and a_tag.has_attr('href') else ''

        url_news = 'https://www.forexfactory.com/' + str(href)

        n = session.get(url_news, timeout=30, headers=headers)
        soup_news = BeautifulSoup(n.content, 'html.parser')

        content = soup_news.select_one('.flexBox.noflex.news__story').text
        
        # Append all the information as a dictionary to news_low
        news_high.append({'Time': time, 'Title': title, 'Impact': impact, 'Content': content})

    df = pd.DataFrame(news_high)

    df['TimeDelta'] = df['Time'].apply(convert_to_timedelta)

    df = df.sort_values(by='TimeDelta', ascending=False)

    return df

def fetch_news_calendar():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}
    u = 'https://www.forexfactory.com/calendar?day=today'

    session = requests.Session()
    r = session.get(u, timeout=30, headers=headers)

    soup = BeautifulSoup(r.content, 'html.parser')

    events_cal = []

    for events in soup.select('.calendar__row'):
        time_elem = events.select_one('.calendar__cell.calendar__time')
        currency_elem = events.select_one('.calendar__cell.calendar__currency')
        title_elem = events.select_one('.calendar__cell.calendar__event')
        actual_elem = events.select_one('.calendar__cell.calendar__actual')
        forecast_elem = events.select_one('.calendar__cell.calendar__forecast')
        previous_elem = events.select_one('.calendar__cell.calendar__previous')
        
        impact_elem = events.select_one('.calendar__cell.calendar__impact')
        impact_class = impact_elem.find('span').get('class') if impact_elem and impact_elem.find('span') else ''
        if impact_class == ['icon', 'icon--ff-impact-red']:
            impact = 'high'
        else:
            impact = ''

        time = time_elem.text if time_elem else ''
        currency = currency_elem.text if currency_elem else ''
        title = title_elem.text if title_elem else ''
        actual = actual_elem.text if actual_elem else ''
        forecast = forecast_elem.text if forecast_elem else ''
        previous = previous_elem.text if previous_elem else ''

        events_cal.append({'Time': time,
                           'Title': title,
                           'Currency': currency,
                           'Impact': impact,
                           'Actual': actual,
                           'Previous': previous,
                           'Forecast': forecast})

    df = pd.DataFrame(events_cal)
    df = df[df['Impact']=='high']
    
    return df

def convert_to_timedelta(s):
    num, unit = s.split()[:-1]
    num = int(num)
    if unit == 'hr':
        return timedelta(hours=num)
    elif unit == 'min':
        return timedelta(minutes=num)

def SentimentAnalysis(df):

    try:
        tokenizer = AutoTokenizer.from_pretrained('ProsusAI/finbert')
        model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

        financial_news=list(df['Content'])
        headlines_list=list(df['Title'])
        content_list=list(df['Content'])

        inputs = tokenizer(financial_news, padding = True, truncation = True, return_tensors='pt')
        outputs = model(**inputs)

        predictions = torch.nn.functional.softmax(outputs.logits, dim=1)

        positive = predictions[:, 0].tolist()
        negative = predictions[:, 1].tolist()
        neutral = predictions[:, 2].tolist()

        table = {'Headline':headlines_list,
                "Positive":positive,
                "Negative":negative, 
                "Neutral":neutral, 
                "Content":content_list}
            
        df = pd.DataFrame(table, columns = ["Headline", "Positive", "Negative", "Neutral", "Content"])

        return df
    except Exception as e:
        print("Error in SentimentAnalysis:", str(e))

def NewsSignal(symbol):
    cal = fetch_news_calendar()
    cal.reset_index(drop=True, inplace=True)
    
    if symbol == 'EURUSD':
        currency_chosen = 'EUR'
        cal = cal[(cal['Currency'] == 'EUR') | (cal['Currency'] == 'USD')]
    elif symbol == 'GBPUSD':
        currency_chosen = 'GBP'
        cal = cal[(cal['Currency'] == 'GBP') | (cal['Currency'] == 'USD')]
    else:
        return

    signal = []
    
    for i, row in cal.iterrows():
        curr_signal = 0
        if row['Actual'] != '':
            actual = float(row['Actual'][:len(row['Actual']) - 1])
            forecast = float(row['Forecast'][:len(row['Forecast']) - 1])
            
            if row['Title'] not in ['Unemployment Claims', 'Unemployment Rate']:
                curr_signal = 1 if actual > forecast else -1 if actual < forecast else 0
            else:
                curr_signal = -1 if actual > forecast else 1 if actual < forecast else 0
            
            if row['Currency'] != currency_chosen:
                curr_signal *= -1
            
        signal.append(curr_signal)

    cal['signal'] = signal

    return cal

running = False
VOLUME = None

def bot_logic(window, SYMBOLS):

    cant_sleep = CantSleep()
    global running
    
    # Add initialized
    last_call_minutes_5 = {symbol: None for symbol in SYMBOLS}
    last_call_minutes_15 = {symbol: None for symbol in SYMBOLS}
    last_call_minutes_30 = {symbol: None for symbol in SYMBOLS}

    signal_m15 = None
    signal_m30 = None
    signal_m5 = None

    latest_calculations = {symbol: {'close_m5': 'Updating...', 
                                    'close_m15': 'Updating...', 
                                    'close_m30' : 'Updating...',
                                    'signal_m5' : 'Updating...', 
                                    'signal_m15' : 'Updating...',
                                    'signal_m30' : 'Updating...',
                                    'tp_1' : 'Updating...',
                                    'tp_2' : 'Updating...',
                                    'tp_3' : 'Updating...',
                                    'tp_4' : 'Updating...',
                                    'tp_5' : 'Updating...',
                                    'sl' : None,
                                    'is_m15_signal' : False,
                                    'is_m30_signal' : False, 
                                    'is_m5_signal' : False,
                                    'signal_news': 'Updating...',} for symbol in SYMBOLS}
        
    already_traded={symbol:False for symbol in SYMBOLS}

    # Create dictionary
    action_dict = {
        1: 'Buy',
        -1: 'Sell',
        0: 'Neutral',
        'Updating...': 'Updating...',
    }

    while running:

        # calculating account exposure
        exposure = {}
        for symbol in SYMBOLS:
            exposure[symbol] = cant_sleep.get_exposure(symbol)

        trades = cant_sleep.get_all_positions()

        '''Get length of trades for the symbol'''

        symbol_trade_lengths = {}

        if 'symbol' in trades.columns:
            # Group by 'symbol' and get counts
            symbol_counts = trades.groupby('symbol').size()
            # Iterate over SYMBOLS list
            for symbol in SYMBOLS:
                # Get the count for the symbol, if it is not in the index, return 0
                symbol_trade_lengths[symbol] = symbol_counts.get(symbol, 0)
        else:
            # If symbol column is not present, set count for all symbols to 0
            for symbol in SYMBOLS:
                symbol_trade_lengths[symbol] = 0

        '''The last of the list is the last of the dataframe'''

        if len(trades) > 0:
            types_current_trades = []
            profit_current_trades = []
            tickets_current_trades = []
            symbols_current_trades = []
            sl_current_trades = []
            tp_current_trades = []
            final_gains_losses = []
            for _, row in trades.iterrows():
                types_current_trades.append(row['type'])
                profit_current_trades.append(row['profit'])
                symbols_current_trades.append(row['symbol'])
                tickets_current_trades.append(int(row['ticket']))
                sl_current_trades.append(row['sl'])
                tp_current_trades.append(row['tp'])
                if row['type']==0:
                    final_gains_losses.append(row['price_current']-row['price_open'])
                else:
                    final_gains_losses.append(row['price_open']-row['price_current'])

        # Compute total profit

        if len(trades) > 0:
            total_profit = round(trades['profit'].sum(), 2)
        else:
            total_profit = 0.0

        if total_profit >= 0:
            window['-PROFIT-'].update(f'{total_profit}', text_color='green')
        else:
            window['-PROFIT-'].update(f'{total_profit}', text_color='red')

        # Get the current minute and time
        current_minute = int(time.strftime('%M'))

        '''Start iterating over each symbol'''

        for symbol in SYMBOLS:

            #### Check if tp is hit (no slippage) and risk management, different levels of tps

            if 0 < symbol_trade_lengths[symbol] <= 1:
                tick = mt5.symbol_info(symbol)
                price = tick.bid
                index = symbols_current_trades.index(symbol)
                volume = exposure[symbol]
                df= pd.DataFrame(mt5.copy_rates_from_pos(symbol, 
                                                mt5.TIMEFRAME_M5, 
                                                1, 
                                                300))
                df['time'] = pd.to_datetime(df['time'], unit='s')
                df = df[['time', 'open', 'high', 'low', 'close', 'tick_volume']]
                df.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
                df['atr']=ATR(df)
                atr = df.atr.iloc[-1]
                if types_current_trades[index] == 0:
                    # Check if stop loss is hit
                    if price <= latest_calculations[symbol]['sl']:
                        result = cant_sleep.close_positions('buy', symbol)
                        profit_trade=(final_gains_losses[index]*100000)*volume
                        msg = f'Trade on {symbol} closed due to stop loss. Profit of about {profit_trade} €.'
                        # send_sms(msg)
                    else:
                        # Check if any TP level is reached
                        for level in range(5, 0, -1):
                            if price >= latest_calculations[symbol][f'tp_{level}']:
                                # If 5th level, close it
                                if level == 5:
                                    result = cant_sleep.close_positions('buy', symbol)
                                    profit_trade=(final_gains_losses[index]*100000)*volume
                                    msg = f'Trade on {symbol} ended with positive profit of about {profit_trade} €.'
                                    # send_sms(msg)
                                elif level >= 2:
                                    mid = (latest_calculations[symbol][f'tp_{level}'] + latest_calculations[symbol][f'tp_{level - 1}'])/2
                                    latest_calculations[symbol]['sl'] = (latest_calculations[symbol][f'tp_{level}'] + mid)/2
                                    latest_calculations[symbol]['tp'] = latest_calculations[symbol][f'tp_{level + 1}']
                                elif level == 1:
                                    latest_calculations[symbol]['sl'] = latest_calculations[symbol][f'tp_{level}'] 
                                    latest_calculations[symbol]['tp'] = latest_calculations[symbol][f'tp_{level + 1}']

                elif types_current_trades[index] == 1:

                    # Check if stop loss is hit
                    if price >= latest_calculations[symbol]['sl']:
                        result = cant_sleep.close_positions('sell', symbol)
                        profit_trade=(final_gains_losses[index]*100000)*volume
                        msg = f'Trade on {symbol} closed due to stop loss. Profit of about {profit_trade} €.'
                        # send_sms(msg)
                        
                    else:
                        # Check if any TP level is reached
                        for level in range(5, 0, -1):
                            if price <= latest_calculations[symbol][f'tp_{level}']:
                                # If 5th level, close it
                                if level == 5:
                                    result = cant_sleep.close_positions('sell', symbol)
                                    profit_trade=(final_gains_losses[index]*100000)*volume
                                    msg = f'Trade on {symbol} ended with positive profit of about {profit_trade} €.'
                                    # send_sms(msg)
                                elif level >= 2:
                                    mid = (latest_calculations[symbol][f'tp_{level}'] + latest_calculations[symbol][f'tp_{level - 1}'])/2
                                    latest_calculations[symbol]['sl'] = (latest_calculations[symbol][f'tp_{level}'] + mid)/2
                                    latest_calculations[symbol]['tp'] = latest_calculations[symbol][f'tp_{level + 1}'] 
                                elif level == 1:
                                    latest_calculations[symbol]['sl'] = latest_calculations[symbol][f'tp_{level}'] 
                                    latest_calculations[symbol]['tp'] = latest_calculations[symbol][f'tp_{level + 1}']

            ## Get volume for the symbol

            VOLUME = cant_sleep.get_volume(symbol)

            # Check if the 5-minute calculation needs to be performed, and get news
            # Only update the latest calculations when a new calculation is performed
            if current_minute % 5 == 0 and current_minute != last_call_minutes_5[symbol] and check_allowed_trading_hours(symbol):
                data = Porte(symbol=symbol, timeframe='M5')
                if data:  # check if data is not None
                    signal_m5, close_m5, sl_m5, tp_m5_1, tp_m5_2, tp_m5_3, tp_m5_4, tp_m5_5 = data
                    last_call_minutes_5[symbol] = current_minute
                    latest_calculations[symbol]['close_m5'] = close_m5  # Update the latest calculation
                    latest_calculations[symbol]['signal_m5'] = signal_m5
                    latest_calculations[symbol]['is_m5_signal']= False
                    already_traded[symbol]=False
                ## News Signals
                df_cal = NewsSignal(symbol)
                if df_cal.empty:
                    signal_news = 0
                else:
                    signal_news = df_cal['signal'].iloc[-1]
                    latest_calculations[symbol]['signal_news'] = signal_news

            # Check if the 15-minute calculation needs to be performed
            if current_minute % 15 == 0 and current_minute != last_call_minutes_15[symbol] and check_allowed_trading_hours(symbol):
                data = Porte(symbol=symbol, timeframe='M15')
                if data:  # check if data is not None
                    signal_m15, close_m15, sl_m15, tp_m15_1, tp_m15_2, tp_m15_3, tp_m15_4, tp_m15_5 = data
                    last_call_minutes_15[symbol] = current_minute
                    latest_calculations[symbol]['close_m15'] = close_m15  # Update the latest calculation
                    latest_calculations[symbol]['signal_m15'] = signal_m15
                    latest_calculations[symbol]['is_m15_signal']= False
                    already_traded[symbol]=False

            # Check if the 30-minute calculation needs to be performed
            if current_minute % 30 == 0 and current_minute != last_call_minutes_30[symbol] and check_allowed_trading_hours(symbol):
                data = Porte(symbol=symbol, timeframe='M30')
                if data:  # check if data is not None
                    signal_m30, close_m30, sl_m30, tp_m30_1, tp_m30_2, tp_m30_3, tp_m30_4, tp_m30_5 = data
                    last_call_minutes_30[symbol] = current_minute
                    latest_calculations[symbol]['close_m30'] = close_m30  # Update the latest calculation
                    latest_calculations[symbol]['signal_m30'] = signal_m30
                    latest_calculations[symbol]['is_m30_signal']= False
                    already_traded[symbol]=False

            '''Close any trades still opened after trading hours'''
            if 0 < symbol_trade_lengths[symbol] <=1 and datetime.now().hour > 21 or datetime.now().weekday() in (5,6):
                index = symbols_current_trades.index(symbol)
                if types_current_trades[index] == 0:
                    result = cant_sleep.close_positions('buy', symbol)
                elif types_current_trades[index] == 1:
                    result = cant_sleep.close_positions('sell', symbol)

            '''Buying logic'''

            if 0 < symbol_trade_lengths[symbol] <=1:
                index = symbols_current_trades.index(symbol)
                volume=exposure[symbol]
                if types_current_trades[index] == 0 and signal_m30 == -1.0 and not latest_calculations[symbol]['is_m30_signal']:
                    result = cant_sleep.close_positions('buy', symbol)
                    profit_trade=(final_gains_losses[index]*100000)*volume
                    msg=f'Trade on {symbol} ended with (about) {profit_trade} €'
                    #send_sms(msg)
                    order_result = cant_sleep.market_order(symbol, VOLUME, 'sell', stoploss=sl_m30)
                    latest_calculations[symbol]['is_m30_signal'] = True
                    latest_calculations[symbol]['is_m15_signal'] = False
                    latest_calculations[symbol]['is_m5_signal'] = False
                    latest_calculations[symbol]['tp_1'] = tp_m30_1
                    latest_calculations[symbol]['tp_2'] = tp_m30_2
                    latest_calculations[symbol]['tp_3'] = tp_m30_3
                    latest_calculations[symbol]['tp_4'] = tp_m30_4
                    latest_calculations[symbol]['tp_5'] = tp_m30_5
                    latest_calculations[symbol]['sl'] = sl_m30
                    msg=f'Selling trade opened on {symbol}, 30 minutes'
                    #send_sms(msg)
                elif types_current_trades[index] == 1 and signal_m30 == 1.0 and not latest_calculations[symbol]['is_m30_signal']:
                    result = cant_sleep.close_positions('sell', symbol)
                    profit_trade=(final_gains_losses[index]*100000)*volume
                    msg=f'Trade on {symbol} ended with (about) {profit_trade} €'
                    #send_sms(msg)
                    order_result = cant_sleep.market_order(symbol, VOLUME, 'buy', stoploss = sl_m30)
                    latest_calculations[symbol]['is_m30_signal'] = True
                    latest_calculations[symbol]['is_m15_signal'] = False
                    latest_calculations[symbol]['is_m5_signal'] = False
                    latest_calculations[symbol]['tp_1'] = tp_m30_1
                    latest_calculations[symbol]['tp_2'] = tp_m30_2
                    latest_calculations[symbol]['tp_3'] = tp_m30_3
                    latest_calculations[symbol]['tp_4'] = tp_m30_4
                    latest_calculations[symbol]['tp_5'] = tp_m30_5
                    latest_calculations[symbol]['sl'] = sl_m30
                    msg=f'Buying trade opened on {symbol}, 30 minutes'
                    #send_sms(msg)
                elif types_current_trades[index] == 0 and signal_m15 == -1.0 and not latest_calculations[symbol]['is_m15_signal']:
                    result = cant_sleep.close_positions('buy', symbol)
                    profit_trade=(final_gains_losses[index]*100000)*volume
                    msg=f'Trade on {symbol} ended with (about) {profit_trade} €'
                    #send_sms(msg)
                    order_result = cant_sleep.market_order(symbol, VOLUME, 'sell', stoploss=sl_m15)
                    latest_calculations[symbol]['is_m30_signal'] = False
                    latest_calculations[symbol]['is_m15_signal'] = True
                    latest_calculations[symbol]['is_m5_signal'] = False
                    latest_calculations[symbol]['tp_1'] = tp_m15_1
                    latest_calculations[symbol]['tp_2'] = tp_m15_2
                    latest_calculations[symbol]['tp_3'] = tp_m15_3
                    latest_calculations[symbol]['tp_4'] = tp_m15_4
                    latest_calculations[symbol]['tp_5'] = tp_m15_5 
                    latest_calculations[symbol]['sl'] = sl_m15
                    msg=f'Selling trade opened on {symbol}, 15 minutes'
                    #send_sms(msg)         
                elif types_current_trades[index] == 1 and signal_m15 == 1.0 and not latest_calculations[symbol]['is_m15_signal']:
                    result = cant_sleep.close_positions('sell', symbol)
                    profit_trade=(final_gains_losses[index]*100000)*volume
                    msg=f'Trade on {symbol} ended with (about) {profit_trade} €'
                    #send_sms(msg)
                    order_result = cant_sleep.market_order(symbol, VOLUME, 'buy', stoploss = sl_m15)
                    latest_calculations[symbol]['is_m30_signal'] = False
                    latest_calculations[symbol]['is_m15_signal'] = True
                    latest_calculations[symbol]['is_m5_signal'] = False
                    latest_calculations[symbol]['tp_1'] = tp_m15_1
                    latest_calculations[symbol]['tp_2'] = tp_m15_2
                    latest_calculations[symbol]['tp_3'] = tp_m15_3
                    latest_calculations[symbol]['tp_4'] = tp_m15_4
                    latest_calculations[symbol]['tp_5'] = tp_m15_5
                    latest_calculations[symbol]['sl'] = sl_m15
                    msg=f'Buying trade opened on {symbol}, 15 minutes'
                    #send_sms(msg)
                elif types_current_trades[index] == 0 and signal_m5 == -1.0 and not latest_calculations[symbol]['is_m5_signal']:
                    result = cant_sleep.close_positions('buy', symbol)
                    profit_trade=(final_gains_losses[index]*100000)*volume
                    msg=f'Trade on {symbol} ended with (about) {profit_trade} €'
                    #send_sms(msg)
                    order_result = cant_sleep.market_order(symbol, VOLUME, 'sell', stoploss=sl_m5)
                    latest_calculations[symbol]['is_m30_signal'] = False
                    latest_calculations[symbol]['is_m15_signal'] = False
                    latest_calculations[symbol]['is_m5_signal'] = True
                    latest_calculations[symbol]['tp_1'] = tp_m5_1
                    latest_calculations[symbol]['tp_2'] = tp_m5_2
                    latest_calculations[symbol]['tp_3'] = tp_m5_3
                    latest_calculations[symbol]['tp_4'] = tp_m5_4
                    latest_calculations[symbol]['tp_5'] = tp_m5_5
                    latest_calculations[symbol]['sl'] = sl_m5
                    msg=f'Selling trade opened on {symbol}, 5 minutes'
                    #send_sms(msg)
                elif types_current_trades[index] == 1 and signal_m5 == 1.0 and not latest_calculations[symbol]['is_m5_signal']:
                    result = cant_sleep.close_positions('sell', symbol)
                    profit_trade=(final_gains_losses[index]*100000)*volume
                    msg=f'Trade on {symbol} ended with (about) {profit_trade} €'
                    #send_sms(msg)
                    order_result = cant_sleep.market_order(symbol, VOLUME, 'buy', stoploss = sl_m5)
                    latest_calculations[symbol]['is_m30_signal'] = False
                    latest_calculations[symbol]['is_m15_signal'] = False
                    latest_calculations[symbol]['is_m5_signal'] = True
                    latest_calculations[symbol]['tp_1'] = tp_m5_1
                    latest_calculations[symbol]['tp_2'] = tp_m5_2
                    latest_calculations[symbol]['tp_3'] = tp_m5_3
                    latest_calculations[symbol]['tp_4'] = tp_m5_4
                    latest_calculations[symbol]['tp_5'] = tp_m5_5
                    latest_calculations[symbol]['sl'] = sl_m5
                    msg=f'Buying trade opened on {symbol}, 5 minutes'
                    #send_sms(msg)

            if symbol_trade_lengths[symbol]==0 and not already_traded[symbol]:
                if signal_m15 == 1.0 and not latest_calculations[symbol]['is_m15_signal']:
                    order_result = cant_sleep.market_order(symbol, VOLUME, 'buy', stoploss = sl_m15)
                    print(order_result)
                    latest_calculations[symbol]['is_m30_signal'] = False
                    latest_calculations[symbol]['is_m15_signal'] = True
                    latest_calculations[symbol]['is_m5_signal'] = False
                    latest_calculations[symbol]['tp_1'] = tp_m15_1
                    latest_calculations[symbol]['tp_2'] = tp_m15_2
                    latest_calculations[symbol]['tp_3'] = tp_m15_3
                    latest_calculations[symbol]['tp_4'] = tp_m15_4
                    latest_calculations[symbol]['tp_5'] = tp_m15_5
                    latest_calculations[symbol]['sl'] = sl_m15
                    msg=f'Buying trade opened on {symbol}, 15 minutes'
                    #send_sms(msg)
                    already_traded[symbol]=True
                elif signal_m5 == 1.0 and not latest_calculations[symbol]['is_m5_signal']:
                    order_result = cant_sleep.market_order(symbol, VOLUME, 'buy', stoploss=sl_m5)
                    print(order_result)
                    latest_calculations[symbol]['is_m30_signal'] = False
                    latest_calculations[symbol]['is_m15_signal'] = False
                    latest_calculations[symbol]['is_m5_signal'] = True
                    latest_calculations[symbol]['tp_1'] = tp_m5_1
                    latest_calculations[symbol]['tp_2'] = tp_m5_2
                    latest_calculations[symbol]['tp_3'] = tp_m5_3
                    latest_calculations[symbol]['tp_4'] = tp_m5_4
                    latest_calculations[symbol]['tp_5'] = tp_m5_5
                    latest_calculations[symbol]['sl'] = sl_m5
                    msg = f'Selling trade opened on {symbol}, 5 minutes'
                    #send_sms(msg) 
                    already_traded[symbol] = True
                elif signal_m30 == 1.0 and not latest_calculations[symbol]['is_m30_signal']:
                    order_result = cant_sleep.market_order(symbol, VOLUME, 'buy', stoploss = sl_m30)
                    print(order_result)
                    latest_calculations[symbol]['is_m30_signal'] = True
                    latest_calculations[symbol]['is_m15_signal'] = False
                    latest_calculations[symbol]['is_m5_signal'] = False
                    latest_calculations[symbol]['tp_1'] = tp_m30_1
                    latest_calculations[symbol]['tp_2'] = tp_m30_2
                    latest_calculations[symbol]['tp_3'] = tp_m30_3
                    latest_calculations[symbol]['tp_4'] = tp_m30_4
                    latest_calculations[symbol]['tp_5'] = tp_m30_5
                    latest_calculations[symbol]['sl'] = sl_m30
                    msg=f'Buying trade opened on {symbol}, 30 minutes'
                    #send_sms(msg)  
                    already_traded[symbol]=True
                elif signal_m15 == -1.0 and not latest_calculations[symbol]['is_m15_signal']:
                    order_result = cant_sleep.market_order(symbol, VOLUME, 'sell', stoploss=sl_m15)
                    print(order_result)
                    latest_calculations[symbol]['is_m30_signal'] = False
                    latest_calculations[symbol]['is_m15_signal'] = True
                    latest_calculations[symbol]['is_m5_signal'] = False
                    latest_calculations[symbol]['tp_1'] = tp_m15_1
                    latest_calculations[symbol]['tp_2'] = tp_m15_2
                    latest_calculations[symbol]['tp_3'] = tp_m15_3
                    latest_calculations[symbol]['tp_4'] = tp_m15_4
                    latest_calculations[symbol]['tp_5'] = tp_m15_5
                    latest_calculations[symbol]['sl'] = sl_m15
                    msg=f'Selling trade opened on {symbol}, 15 minutes'
                    #send_sms(msg)
                    already_traded[symbol]=True
                elif signal_m5 == -1.0 and not latest_calculations[symbol]['is_m5_signal']:
                    order_result = cant_sleep.market_order(symbol, VOLUME, 'sell', stoploss=sl_m5)
                    latest_calculations[symbol]['is_m30_signal'] = False
                    latest_calculations[symbol]['is_m15_signal'] = False
                    latest_calculations[symbol]['is_m5_signal'] = True
                    latest_calculations[symbol]['tp_1'] = tp_m5_1
                    latest_calculations[symbol]['tp_2'] = tp_m5_2
                    latest_calculations[symbol]['tp_3'] = tp_m5_3
                    latest_calculations[symbol]['tp_4'] = tp_m5_4
                    latest_calculations[symbol]['tp_5'] = tp_m5_5
                    latest_calculations[symbol]['sl'] = sl_m5
                    msg = f'Selling trade opened on {symbol}, 5 minutes'
                    #send_sms(msg) 
                    already_traded[symbol] = True
                elif signal_m30 == -1.0 and not latest_calculations[symbol]['is_m30_signal']:
                    order_result = cant_sleep.market_order(symbol, VOLUME, 'sell', stoploss=sl_m30)
                    print(order_result)
                    latest_calculations[symbol]['is_m30_signal'] = True
                    latest_calculations[symbol]['is_m15_signal'] = False
                    latest_calculations[symbol]['is_m5_signal'] = False
                    latest_calculations[symbol]['tp_1'] = tp_m30_1
                    latest_calculations[symbol]['tp_2'] = tp_m30_2
                    latest_calculations[symbol]['tp_3'] = tp_m30_3
                    latest_calculations[symbol]['tp_4'] = tp_m30_4
                    latest_calculations[symbol]['tp_5'] = tp_m30_5
                    latest_calculations[symbol]['sl'] = sl_m30
                    msg=f'Selling trade opened on {symbol}, 30 minutes'
                    #send_sms(msg)
                    already_traded[symbol]=True

        '''End of for loop'''

        current_time = datetime.now().strftime('%Y:%D          %H:%M:%S')

        output_text = f"Current time: {current_time}\n"
        output_text += "----------------------------------------\n"
        for symbol in SYMBOLS:
            output_text += f"----------------{symbol}------------------\n"
            output_text += f"Exposure : {exposure[symbol]}\n"
            output_text += "----------------------------------------\n"
            output_text += f"Current signal for 5 minutes : {action_dict[latest_calculations[symbol]['signal_m5']]}\n"
            output_text += f"Current signal for 15 minutes : {action_dict[latest_calculations[symbol]['signal_m15']]}\n"
            output_text += f"Current signal for 30 minutes : {action_dict[latest_calculations[symbol]['signal_m30']]}\n"
            output_text += f"Current news signal : {action_dict[latest_calculations[symbol]['signal_news']]}\n"
            output_text += "----------------------------------------\n"             
        output_text += f"Trades : {len(trades)}\n"

        window['-OUTPUT-'].update(output_text)

        # Refresh the window to update the interface
        window.refresh()
        
        # update every 1 second
        time.sleep(1)

#-----------------------------------------------------GUI----------------------------------------------------------#

time_start_bot = None

# Predefined list of symbols
PREDEFINED_SYMBOLS = [
    'EURUSD', 'GBPUSD', 'USDCAD', 'USDJPY', 
    'USDCHF', 'GOLD', 'SILVER', '[ASX200]', 
    '[CAC40]', '[DAX40]', '[DJI30]', '[FTSE100]', 
    '[NQ100]', 'CRUDOIL', 'BRENT', 'NGAS', 
    'AAPL', 'AMZN'
]

# Define a look and feel theme for the GUI
sg.LOOK_AND_FEEL_TABLE['DarkBlue'] = {
    'BACKGROUND': '#2C2F33',
    'TEXT': '#C7C7C7',
    'INPUT': '#2D3E50',
    'TEXT_INPUT': '#C7C7C7',
    'SCROLL': '#C7C7C7',
    'BUTTON': ('white', '#7289DA'),
    'PROGRESS': ('#01826B', '#D0D0D0'),
    'BORDER': 1,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0,
}

# Set the theme
sg.theme('DarkBlue')

# File where we will save the login data
login_data_file = 'login_data_file.json'

def get_login_data():
    try:
        with open(login_data_file, 'r') as f:
            data = json.load(f)
            return data['login'], data['password'], data['server']
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return "", "", ""

def save_login_data(login, password, server):
    data = {
        'login': login,
        'password': password,
        'server': server
    }
    with open(login_data_file, 'w') as f:
        json.dump(data, f)

def run_flask_app(df1, df2):
    app = Flask(__name__)
    @app.route('/')
    def index():
        return render_template_string("""
        <h1>News Calendar and Sentiment Analysis</h1>
        <h2>News Calendar</h2>
        {{ df1|safe }}
        <h2>Sentiment Analysis</h2>
        {{ df2|safe }}
        """, df1=df1.to_html(), df2=df2.to_html())
    app.run(port=5000, debug=False)


def login_window():
    # Initialize values with saved data
    login, password, server = get_login_data()

    layout = [[sg.Text('Login:'), sg.Input(login, key='-LOGIN-', size=(20,1))],
              [sg.Text('Password:'), sg.Input(password, key='-PASSWORD-', size=(20,1), password_char='*')],
              [sg.Text('Server:'), sg.Combo(['AdmiralMarkets-Demo', 'AdmiralMarkets-Live'], default_value=server, key='-SERVER-', size=(20,1))],
              [sg.Checkbox('Remember me', key='-REMEMBER-', default=bool(login))],
              [sg.Button('Login'), sg.Button('Exit')]]

    window = sg.Window('Login to MetaTrader', layout)

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Exit'):
            mt5.shutdown()
            window.close()
            return False
        elif event == 'Login':
            login = values['-LOGIN-']
            password = values['-PASSWORD-']
            server = values['-SERVER-']

            # Try to initialize MT5 and login
            if not mt5.initialize():
                sg.Popup('MT5 initialization failed')
                continue
            elif not mt5.login(int(login), str(password), server=str(server)):
                sg.Popup('MT5 login failed')
                continue

            if values['-REMEMBER-']:
                save_login_data(login, password, server)

            window.close()
            return True

def symbol_selection_window():
    SYMBOLS = []
    # Open a new window to select symbols
    symbol_layout = [
        [sg.Text('Select Symbols:', font='Any 12')],
        [sg.Listbox(PREDEFINED_SYMBOLS, size=(40, 10), key='-SYMBOL-LIST-', select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, default_values=SYMBOLS)],
        [sg.Button('Delete', button_color=('white', '#7289DA')), sg.Button('Done', button_color=('white', '#7289DA'))]
    ]

    symbol_window = sg.Window('Symbol Selection', symbol_layout)

    while True:
        symbol_event, symbol_values = symbol_window.read()

        if symbol_event == sg.WINDOW_CLOSED or symbol_event == 'Done':
            selected = symbol_values['-SYMBOL-LIST-']
            SYMBOLS = [symbol for symbol in selected]  # Update SYMBOLS with the selected symbols
            break
        elif symbol_event == 'Delete':
            selected = symbol_values['-SYMBOL-LIST-']
            for symbol in selected:
                if symbol in SYMBOLS:
                    SYMBOLS.remove(symbol)

        symbol_window['-SYMBOL-LIST-'].update(values=PREDEFINED_SYMBOLS, set_to_index=[PREDEFINED_SYMBOLS.index(symbol) for symbol in SYMBOLS])

    symbol_window.close()
    return SYMBOLS  # Return the selected symbols

# Create the login window
if not os.path.exists(login_data_file):
    sg.Popup('Login data not found', 'Please enter your credentials.')
    login_result = login_window()
else:
    login_result = login_window()

if login_result:
    running = False

    # Create columns for better layout management
    col1 = sg.Column(
        [[sg.Text("Values:", font='Any 14', expand_x=True)],
        [sg.Text("Selected Symbol(s): "), sg.Text(size=(30, 1), key='-SYMBOLS-', expand_x=True)],
        [sg.Text('Profit: ', font='Any 12', expand_x=True), sg.Text('', key='-PROFIT-', font='Any 12', expand_x=True)],
        [sg.Button('Add Symbols', key='-ADD-', button_color=('white', '#7289DA'), expand_x=True),
        sg.Button('Start', key='-START-', button_color=('white', '#7289DA'), expand_x=True),
        sg.Button('Stop', key='-STOP-', button_color=('white', '#7289DA'), disabled=True, expand_x=True)],
        [sg.Output(size=(80, 20), key='-OUTPUT-', expand_x=True)]
        ],
        vertical_alignment='top',
    )

    layout = [
        [col1],
        [sg.Button('Exit', button_color=('white', '#7289DA')), 
        sg.Button('Past Results', key='-PASTRESULTS-', button_color=('white', '#7289DA')), 
        sg.Button('News and Calendar', key='-NEWSCALENDAR-', button_color=('white', '#7289DA'))]  
    ]
    window = sg.Window('Obawarqué', layout, finalize=True, resizable=True)

    while True:
        event, values = window.read(timeout=10000)

        if event == sg.WINDOW_CLOSED or event == 'Exit':
            mt5.shutdown()
            break
        elif event == '-NEWSCALENDAR-':
            df1 = fetch_news_calendar()
            df1.reset_index(drop=True, inplace=True)
            df_news = fetch_news()
            df2 = SentimentAnalysis(df_news)
            flask_thread = Thread(target=run_flask_app, args=(df1, df2))
            flask_thread.daemon = True
            flask_thread.start()

            webbrowser.open("http://127.0.0.1:5000/")

        elif event == '-ADD-':
            if running:  # If bot is running, ignore the add event
                continue
            # Get selected symbols
            SYMBOLS = symbol_selection_window()
            window['-SYMBOLS-'].update(', '.join(SYMBOLS))
        elif event == '-START-':
            if not SYMBOLS:  
                sg.Popup('Alert', 'Please add at least one symbol before starting.')
                continue
            if not running: 
                time_start_bot = datetime.now()  # Check if the bot is not already running

                time_start_bot=datetime.now()
                running = True  # Set the running flag to True
                window['-START-'].update(button_color=('white', 'grey'))  # Change button color to grey
                window['-STOP-'].update(disabled=False)
                window['-ADD-'].update(disabled=True, button_color=('white', 'grey'))  # disable and grey 'Add Symbols' button
                bot_thread = Thread(target=bot_logic, args=(window, SYMBOLS))
                bot_thread.start()
        elif event == '-STOP-':
            if running:  # Check if the bot is running
                running = False  # Set the running flag to False to stop the bot
                window['-START-'].update(disabled=False, button_color=('white', '#7289DA'))  # Change button color back
                window['-STOP-'].update(disabled=True)
                window['-ADD-'].update(disabled=False, button_color=('white', '#7289DA'))  # enable 'Add Symbols' button
        elif event == '-PASTRESULTS-':
            # Bring up the symbol selection window for the user to select a symbol
            plot_symbols = symbol_selection_window()

            # If the user doesn't select any symbols, show a popup and continue
            if not plot_symbols:
                sg.Popup('Alert', 'Please select at least one symbol before plotting.')
                continue

            # Popup to inform the user about the processing time
            sg.popup_auto_close('Computations are being done...', auto_close_duration=5, non_blocking=True)

            # Now we start the plot in a separate thread with the selected symbols
            Thread(target=Plot, args=(plot_symbols,)).start()


    window.close()
else:
    quit()

