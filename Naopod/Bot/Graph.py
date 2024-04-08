import plotly.graph_objects as go
import warnings
from pandas.errors import SettingWithCopyWarning
from Indicators import MA

from minette_graph import FinalStrategy
from evaluation_graph import evaluate_strategy

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

#---------------------------------------------------------------------------------------------------#

def Plot(symbols):

    for symbol in symbols:
        if symbol in ['EURUSD', 'GBPUSD', 'USDCAD', 'USDCHF']:
            volume = 100000
        elif symbol in ['[ASX200]','[NQ100]', '[CAC40]', '[DAX40]', '[DJI30]', '[FTSE100]', 'CRUDOIL', 'BRENT', 'NGAS', 'AAPL', 'AMZN']:
            volume = 3
        elif symbol in ['GOLD', 'SILVER']:
            volume = 0.5
        elif symbol == 'USDJPY':
            volume = 1
        grosses_couilles = FinalStrategy(symbol)
        grosses_couilles = evaluate_strategy(grosses_couilles,volume)
        grosses_couilles = grosses_couilles.sort_index()

        grosses_couilles['MA'] = MA(grosses_couilles, n=21)

        # Fill NaN values with 0
        grosses_couilles['final_signal_M5'] = grosses_couilles['final_signal_M5'].fillna(0)
        grosses_couilles['final_signal_M15'] = grosses_couilles['final_signal_M15'].fillna(0)
        grosses_couilles['final_signal_M30'] = grosses_couilles['final_signal_M30'].fillna(0)
        grosses_couilles['final_sl_M5'] = grosses_couilles['final_sl_M5'].fillna(0)
        grosses_couilles['final_sl_M15'] = grosses_couilles['final_sl_M15'].fillna(0)
        grosses_couilles['final_sl_M30'] = grosses_couilles['final_sl_M30'].fillna(0)
        grosses_couilles['final_tp_M5'] = grosses_couilles['final_tp_M5'].fillna(0)
        grosses_couilles['final_tp_M15'] = grosses_couilles['final_tp_M15'].fillna(0)
        grosses_couilles['final_tp_M30'] = grosses_couilles['final_tp_M30'].fillna(0)

        grosses_couilles['prev_close_m5'] = grosses_couilles['Close'].shift(-1)
        grosses_couilles['prev_close_m15'] = grosses_couilles['Close'].shift(-1)
        grosses_couilles['prev_close_m30'] = grosses_couilles['Close'].shift(-1)

        fig = go.Figure(data=[
        go.Scatter(
            x=grosses_couilles.index,
            y=grosses_couilles['MA'],
            mode='lines',
            line=dict(color='purple'),
            name='MA'
        ),
        go.Candlestick(
        x=grosses_couilles.index,
        open=grosses_couilles['Open'],
        high=grosses_couilles['High'],  
        low=grosses_couilles['Low'],
        close=grosses_couilles['Close'],
        showlegend=False
        ),
        go.Scatter(
            x=grosses_couilles[grosses_couilles['final_signal_M5'] == 1].index,
            y=grosses_couilles[grosses_couilles['final_signal_M5'] == 1]['Open'],
            marker_symbol='arrow-up',
            mode='markers',
            marker=dict(size=10, color='Blue'),
            name='Buy_M5'
        ),
        go.Scatter(
            x=grosses_couilles[grosses_couilles['final_signal_M5'] == -1].index,
            y=grosses_couilles[grosses_couilles['final_signal_M5'] == -1]['Open'],
            marker_symbol='arrow-down',
            mode='markers',
            marker=dict(size=10, color='Black'),
            name='Sell_M5'
        ),
        go.Scatter(
            x=grosses_couilles[grosses_couilles['final_signal_M15'] == 1].index,
            y=grosses_couilles[grosses_couilles['final_signal_M15'] == 1]['Open'],
            marker_symbol='arrow-up',
            mode='markers',
            marker=dict(size=10, color='Blue'),
            name='Buy_M15'
        ),
        go.Scatter(
            x=grosses_couilles[grosses_couilles['final_signal_M15'] == -1].index,
            y=grosses_couilles[grosses_couilles['final_signal_M15'] == -1]['Open'],
            marker_symbol='arrow-down',
            mode='markers',
            marker=dict(size=10, color='Black'),
            name='Sell_M15'
        ),
        go.Scatter(
            x=grosses_couilles[grosses_couilles['final_signal_M30'] == 1].index,
            y=grosses_couilles[grosses_couilles['final_signal_M30'] == 1]['Open'],
            marker_symbol='arrow-up',
            mode='markers',
            marker=dict(size=10, color='Blue'),
            name='Buy_M30'
        ),
        go.Scatter(
            x=grosses_couilles[grosses_couilles['final_signal_M30'] == -1].index,
            y=grosses_couilles[grosses_couilles['final_signal_M30'] == -1]['Open'],
            marker_symbol='arrow-down',
            mode='markers',
            marker=dict(size=10, color='Black'),
            name='Sell_M30'
        )])

        # First, create a boolean mask
        trade_mask = (grosses_couilles['final_signal_M5'] != 0) | (grosses_couilles['final_signal_M15'] != 0) | (grosses_couilles['final_signal_M30'] != 0)

        # Then, compute the number of trades
        num_trades = trade_mask.sum()

        fig.update_layout(
            autosize=False,
            width=1200,
            height=900,
            paper_bgcolor='white',
            plot_bgcolor='white',
            title={
                'text': f"{symbol} (Profit Sum: {grosses_couilles['profit'].sum():.2f}, Perc wins: {round(len(grosses_couilles[grosses_couilles['profit']>0])/len(grosses_couilles[grosses_couilles['profit']!=0]), 2)}, Avg win: {round(grosses_couilles[grosses_couilles['profit']>0]['profit'].mean(), 2)}, Avg loss: {round(grosses_couilles[grosses_couilles['profit'] < 0]['profit'].mean(), 2)}, Num trades: {num_trades})",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )

        # Initialize shapes
        shapes = []
        current_signal = None
        current_sl = None
        current_tp = None

        for i in range(len(grosses_couilles)):
            new_signal = None
            new_sl = None
            new_tp = None
            new_open = None  # This will store the appropriate close price depending on the signal's timeframe
            
            # Check for new signals from highest to lowest timeframe
            if grosses_couilles['final_signal_M30'].iloc[i] != 0:  # M30 signal
                new_signal = grosses_couilles['final_signal_M30'].iloc[i]
                new_sl = grosses_couilles['final_sl_M30'].iloc[i]
                new_tp = grosses_couilles['final_tp_M30'].iloc[i]
                new_open = grosses_couilles['Open'].iloc[i]
            elif grosses_couilles['final_signal_M15'].iloc[i] != 0:  # M15 signal
                new_signal = grosses_couilles['final_signal_M15'].iloc[i]
                new_sl = grosses_couilles['final_sl_M15'].iloc[i]
                new_tp = grosses_couilles['final_tp_M15'].iloc[i]
                new_open = grosses_couilles['Open'].iloc[i]
            elif grosses_couilles['final_signal_M5'].iloc[i] != 0:  # M5 signal
                new_signal = grosses_couilles['final_signal_M5'].iloc[i]
                new_sl = grosses_couilles['final_sl_M5'].iloc[i]
                new_tp = grosses_couilles['final_tp_M5'].iloc[i]
                new_open = grosses_couilles['Open'].iloc[i]

            # If there's a current signal, extend the rectangles
            if current_signal is not None:
                shapes[-2]['x1'] = shapes[-1]['x1'] = grosses_couilles.index[i]

                # Check if SL/TP is hit
                if current_signal == 1:  # Buy signal
                    if (current_tp is not None and grosses_couilles['High'].iloc[i] >= current_tp) or \
                       (current_sl is not None and grosses_couilles['Low'].iloc[i] <= current_sl):
                        current_signal = None
                elif current_signal == -1:  # Sell signal
                    if (current_tp is not None and grosses_couilles['Low'].iloc[i] <= current_tp) or \
                       (current_sl is not None and grosses_couilles['High'].iloc[i] >= current_sl):
                        current_signal = None
            
            # If there's a new signal and it's either the first signal or in the opposite direction of the current signal
            if new_signal is not None and (current_signal is None or current_signal != new_signal):
                current_signal = new_signal
                current_sl = new_sl
                current_tp = new_tp
                shapes.extend([{
                    'type': 'rect',
                    'xref': 'x',
                    'yref': 'y',
                    'x0': grosses_couilles.index[i],
                    'y0': new_open,  # Changed from grosses_couilles['Close'].iloc[i]
                    'x1': grosses_couilles.index[i],
                    'y1': current_sl,
                    'fillcolor': 'Red',
                    'opacity': 0.5,
                    'line': {
                        'width': 2,
                    },
                },
                {
                    'type': 'rect',
                    'xref': 'x',
                    'yref': 'y',
                    'x0': grosses_couilles.index[i],
                    'y0': new_open,  # Changed from grosses_couilles['Close'].iloc[i]
                    'x1': grosses_couilles.index[i],
                    'y1': current_tp,
                    'fillcolor': 'Green',
                    'opacity': 0.5,
                    'line': {
                        'width': 2,
                    },
                }])


        fig.update_layout(shapes=shapes)

        annotations = []
        # Add scatter plots of profit values
        for i in range(len(grosses_couilles)):
            if grosses_couilles['profit'].iloc[i] != 0:  # Only plot at the end of a trade

                annotations.append(
                    go.layout.Annotation(
                        x=grosses_couilles.index[i],
                        y=grosses_couilles['Close'].iloc[i],
                        xref="x",
                        yref="y",
                        text=f'Profit: {grosses_couilles["profit"].iloc[i]:.2f}',  # Use <br> for line breaks
                        showarrow=False,
                    )
                )


        fig.update_layout(annotations=annotations)

        fig.show()

###-----------------------------------------------------------------------------------------------------------------------------------------------------------###

