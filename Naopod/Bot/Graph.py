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
        final_df = FinalStrategy(symbol)
        final_df = evaluate_strategy(final_df,volume)
        final_df = final_df.sort_index()

        final_df['MA'] = MA(final_df, n=21)

        # Fill NaN values with 0
        final_df['final_signal_M5'] = final_df['final_signal_M5'].fillna(0)
        final_df['final_signal_M15'] = final_df['final_signal_M15'].fillna(0)
        final_df['final_signal_M30'] = final_df['final_signal_M30'].fillna(0)
        final_df['final_sl_M5'] = final_df['final_sl_M5'].fillna(0)
        final_df['final_sl_M15'] = final_df['final_sl_M15'].fillna(0)
        final_df['final_sl_M30'] = final_df['final_sl_M30'].fillna(0)
        final_df['final_tp_M5'] = final_df['final_tp_M5'].fillna(0)
        final_df['final_tp_M15'] = final_df['final_tp_M15'].fillna(0)
        final_df['final_tp_M30'] = final_df['final_tp_M30'].fillna(0)

        final_df['prev_close_m5'] = final_df['Close'].shift(-1)
        final_df['prev_close_m15'] = final_df['Close'].shift(-1)
        final_df['prev_close_m30'] = final_df['Close'].shift(-1)

        fig = go.Figure(data=[
        go.Scatter(
            x=final_df.index,
            y=final_df['MA'],
            mode='lines',
            line=dict(color='purple'),
            name='MA'
        ),
        go.Candlestick(
        x=final_df.index,
        open=final_df['Open'],
        high=final_df['High'],  
        low=final_df['Low'],
        close=final_df['Close'],
        showlegend=False
        ),
        go.Scatter(
            x=final_df[final_df['final_signal_M5'] == 1].index,
            y=final_df[final_df['final_signal_M5'] == 1]['Open'],
            marker_symbol='arrow-up',
            mode='markers',
            marker=dict(size=10, color='Blue'),
            name='Buy_M5'
        ),
        go.Scatter(
            x=final_df[final_df['final_signal_M5'] == -1].index,
            y=final_df[final_df['final_signal_M5'] == -1]['Open'],
            marker_symbol='arrow-down',
            mode='markers',
            marker=dict(size=10, color='Black'),
            name='Sell_M5'
        ),
        go.Scatter(
            x=final_df[final_df['final_signal_M15'] == 1].index,
            y=final_df[final_df['final_signal_M15'] == 1]['Open'],
            marker_symbol='arrow-up',
            mode='markers',
            marker=dict(size=10, color='Blue'),
            name='Buy_M15'
        ),
        go.Scatter(
            x=final_df[final_df['final_signal_M15'] == -1].index,
            y=final_df[final_df['final_signal_M15'] == -1]['Open'],
            marker_symbol='arrow-down',
            mode='markers',
            marker=dict(size=10, color='Black'),
            name='Sell_M15'
        ),
        go.Scatter(
            x=final_df[final_df['final_signal_M30'] == 1].index,
            y=final_df[final_df['final_signal_M30'] == 1]['Open'],
            marker_symbol='arrow-up',
            mode='markers',
            marker=dict(size=10, color='Blue'),
            name='Buy_M30'
        ),
        go.Scatter(
            x=final_df[final_df['final_signal_M30'] == -1].index,
            y=final_df[final_df['final_signal_M30'] == -1]['Open'],
            marker_symbol='arrow-down',
            mode='markers',
            marker=dict(size=10, color='Black'),
            name='Sell_M30'
        )])

        # First, create a boolean mask
        trade_mask = (final_df['final_signal_M5'] != 0) | (final_df['final_signal_M15'] != 0) | (final_df['final_signal_M30'] != 0)

        # Then, compute the number of trades
        num_trades = trade_mask.sum()

        fig.update_layout(
            autosize=False,
            width=1200,
            height=900,
            paper_bgcolor='white',
            plot_bgcolor='white',
            title={
                'text': f"{symbol} (Profit Sum: {final_df['profit'].sum():.2f}, Perc wins: {round(len(final_df[final_df['profit']>0])/len(final_df[final_df['profit']!=0]), 2)}, Avg win: {round(final_df[final_df['profit']>0]['profit'].mean(), 2)}, Avg loss: {round(final_df[final_df['profit'] < 0]['profit'].mean(), 2)}, Num trades: {num_trades})",
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

        for i in range(len(final_df)):
            new_signal = None
            new_sl = None
            new_tp = None
            new_open = None  # This will store the appropriate close price depending on the signal's timeframe
            
            # Check for new signals from highest to lowest timeframe
            if final_df['final_signal_M30'].iloc[i] != 0:  # M30 signal
                new_signal = final_df['final_signal_M30'].iloc[i]
                new_sl = final_df['final_sl_M30'].iloc[i]
                new_tp = final_df['final_tp_M30'].iloc[i]
                new_open = final_df['Open'].iloc[i]
            elif final_df['final_signal_M15'].iloc[i] != 0:  # M15 signal
                new_signal = final_df['final_signal_M15'].iloc[i]
                new_sl = final_df['final_sl_M15'].iloc[i]
                new_tp = final_df['final_tp_M15'].iloc[i]
                new_open = final_df['Open'].iloc[i]
            elif final_df['final_signal_M5'].iloc[i] != 0:  # M5 signal
                new_signal = final_df['final_signal_M5'].iloc[i]
                new_sl = final_df['final_sl_M5'].iloc[i]
                new_tp = final_df['final_tp_M5'].iloc[i]
                new_open = final_df['Open'].iloc[i]

            # If there's a current signal, extend the rectangles
            if current_signal is not None:
                shapes[-2]['x1'] = shapes[-1]['x1'] = final_df.index[i]

                # Check if SL/TP is hit
                if current_signal == 1:  # Buy signal
                    if (current_tp is not None and final_df['High'].iloc[i] >= current_tp) or \
                       (current_sl is not None and final_df['Low'].iloc[i] <= current_sl):
                        current_signal = None
                elif current_signal == -1:  # Sell signal
                    if (current_tp is not None and final_df['Low'].iloc[i] <= current_tp) or \
                       (current_sl is not None and final_df['High'].iloc[i] >= current_sl):
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
                    'x0': final_df.index[i],
                    'y0': new_open,  # Changed from final_df['Close'].iloc[i]
                    'x1': final_df.index[i],
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
                    'x0': final_df.index[i],
                    'y0': new_open,  # Changed from final_df['Close'].iloc[i]
                    'x1': final_df.index[i],
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
        for i in range(len(final_df)):
            if final_df['profit'].iloc[i] != 0:  # Only plot at the end of a trade

                annotations.append(
                    go.layout.Annotation(
                        x=final_df.index[i],
                        y=final_df['Close'].iloc[i],
                        xref="x",
                        yref="y",
                        text=f'Profit: {final_df["profit"].iloc[i]:.2f}',  # Use <br> for line breaks
                        showarrow=False,
                    )
                )


        fig.update_layout(annotations=annotations)

        fig.show()

###-----------------------------------------------------------------------------------------------------------------------------------------------------------###

