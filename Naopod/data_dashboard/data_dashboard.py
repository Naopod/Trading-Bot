import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import MetaTrader5 as mt
import numpy as np
from statsmodels.tsa.stattools import acf, pacf
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from functions import get_ohlc, get_obaw_data

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR], suppress_callback_exceptions=True)

## Loging in to the account

mt.initialize()

login = 30549258
password = 'DevenirRiche07!'
server = 'AdmiralMarkets-Live'
mt.login(login, password, server)

## Load data

df_stats_obaw = get_obaw_data()
df = get_ohlc(symbol='EURUSD')

df_eur = get_ohlc('EURUSD')
df_gbp = get_ohlc('GBPUSD')
df_gold = get_ohlc('GOLD')

## Basic stats

# Overall Profits

df_stats_obaw['pnl'] = df_stats_obaw['Profits'].cumsum()

fig_overall_profits = px.line(df_stats_obaw,
                            x='Time',
                            y='pnl', 
                            title='Overall Cumulative Profits', 
                            labels={'Time': 'Time',
                            'pnl': 'Profits'},
                            template="plotly_dark")

# Winning trades per symbol

df_stats_obaw['is_win_trade'] = df_stats_obaw['Profits'].apply(lambda x: 1 if x > 0 else 0)

grouped = df_stats_obaw.groupby('Symbol').agg(
    total_trades=pd.NamedAgg(column='is_win_trade', aggfunc='count'),
    winning_trades=pd.NamedAgg(column='is_win_trade', aggfunc='sum')
)

grouped=grouped.reset_index()
grouped.rename(columns={15:'Symbol'}, inplace=True)

# Calculate the percentage of winning trades
grouped['perc_winning_trades'] = (grouped['winning_trades'] / grouped['total_trades']) * 100

fig_share_symbol_wins = px.scatter(
    data_frame=grouped,
    x='total_trades',
    y='winning_trades',
    size='perc_winning_trades',
    labels={'total_trades':'Total Numbers', 'winning_trades':'Number of winning trades'},
    color='Symbol',
    hover_name='Symbol',
    template='plotly_dark',
    title='Share of winning trades per symbols'
)

## Correlation between markets

price_eur = df_eur['Close']
price_gbp = df_gbp['Close']
price_gold = df_gold['Close']

df_prices = pd.concat([price_eur, price_gbp, price_gold], axis=1)
df_prices.columns = ['EURUSD', 'GBPUSD', 'GOLD']

df_prices_corr = df_prices.corr()

fig_corr_markets = go.Figure(data=[
    go.Heatmap(
        x=df_prices_corr.columns,
        y=df_prices_corr.index,
        z=np.array(df_prices_corr),
        text=df_prices_corr.values,
        texttemplate='%{text:.2f}',
        colorscale='Viridis'
    )
])

fig_corr_markets.update_layout(
    title='Correlations between markets',
    template="plotly_dark",
)

## App Layout

app.layout = html.Div([

    html.H1('Data Analytics', style={'text-align':'center'}),
    
    dbc.Tabs([
        dbc.Tab(label='Statistics of Obawarqué', tab_id='tab-obaw'),
        dbc.Tab(label='Statistics of the Markets', tab_id='tab-market'),
    ], id='tabs', active_tab='tab-obaw'),
    
    html.Div(id='tab-content')
])

@app.callback(
    Output('tab-content', 'children'),
    [Input('tabs', 'active_tab')]
)

def render_content(tab):
    if tab == 'tab-obaw':
        return html.Div([
            html.H2('Profits analysis'),
            dcc.Graph(figure=fig_overall_profits),
            html.Br(),

            dcc.Dropdown(id='slct_symbol',
                        options=[
                            {'label':'EURUSD', 'value': 'EURUSD'},
                            {'label': 'GBPUSD', 'value':'GBPUSD'},
                            {'label': 'GOLD', 'value': 'GOLD'}],
                        multi=False,
                        value='EURUSD',   
                        style={'width': '40%'}
                        ),
            html.Div(id='output_container', children=[]),

            html.Div([
            dcc.Graph(id='profit_graph_symbol', style={'display': 'inline-block', 'width': '49%'}),
            dcc.Graph(id='profit_hist_symbol', style={'display': 'inline-block', 'width': '49%'})
            ]),

            html.Br(),

            dcc.Graph(figure=fig_share_symbol_wins),
        ])
    
    elif tab == 'tab-market':
        return html.Div([
            html.H2('Market Statistics'),
            dcc.Graph(figure=fig_corr_markets),
            html.Br(),
            dcc.Dropdown(id='slct_market',
                         options=[
                             {'label':'EURUSD', 'value':'EURUSD'},
                             {'label':'GBPUSD', 'value':'GBPUSD'},
                             {'label':'GOLD', 'value':'GOLD'}],
                        multi=False,
                        value='EURUSD',
                        style={'width':'40%'}
                        ),
            html.Div(id='output_container_market', children=[]),

            html.Div([
                dcc.Graph(id='acf_symbol', style={'display':'inline-block', 'width':'49%'}),
                dcc.Graph(id='pacf_symbol', style={'display': 'inline-block', 'width': '49%'})
            ]),

            html.Br(),

            dcc.Dropdown(id='slct_N',
                         options=[
                             {'label':'1 cluster', 'value':1},
                             {'label':'2 clusters', 'value':2},
                             {'label':'3 clusters', 'value':3},
                             {'label':'4 clusters', 'value':4}],
                        multi=False,
                        value=3,
                        style={'width':'40%'}
                        ),
            html.Div(id='output_container_N', children=[]),

            dcc.Graph(id='cluster_symbol')
        ])


## Callbacks : Connect the Plotly graphs with Dash Components

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='profit_graph_symbol', component_property='figure'),
     Output(component_id='profit_hist_symbol', component_property='figure')],
    [Input(component_id='slct_symbol', component_property='value')]
)

def upgrade_graph_prof_symbol(option_slctd):

    container = 'The symbol chosen by the user is: {}'.format(option_slctd)

    dff = df_stats_obaw.copy()
    dff = dff[dff['Symbol']==option_slctd]

    ## General Profits per symbol
    dff['pnl'] = dff['Profits'].cumsum()

    ## Aggregated Profits per symbol 
    agg_symb_prof = dff['Profits'].sum()

    # Line

    fig_line = px.line(
        dff, 
        x='Time', 
        y='pnl',
        title=f'Cumulative Profits for the symbol: {option_slctd}',
        labels={'Time': 'Time',
                 'pnl': 'Profits'},
        template='plotly_dark'
        )
    
    # Histogram
    fig_hist = go.Figure(
    data=[
        go.Bar(
            x=[option_slctd],
            y=[agg_symb_prof]
        )
    ],
    layout=go.Layout(
        title=f'Aggregated Profits for the symbol: {option_slctd}',
        xaxis=dict(title='Symbol'),
        yaxis=dict(title='Total Profits'),
        template='plotly_dark'
    )
    )
    
    return container, fig_line, fig_hist

@app.callback(
    [Output(component_id='output_container_market', component_property='children'),
     Output(component_id='acf_symbol', component_property='figure'),
     Output(component_id='pacf_symbol', component_property='figure')],
    [Input(component_id='slct_market', component_property='value')]
)

def upgrade_acf_pacf(option_slctd):

    container =  'The market chosen by the user is: {}'.format(option_slctd)

    df = get_ohlc(option_slctd)

    # Compute ACF and PACF
    lag_acf = acf(df['Close'], nlags=5)
    lag_pacf = pacf(df['Close'], nlags=5, method='ols')
    
    # Create Plotly figures
    fig_acf = go.Figure()
    fig_acf.add_trace(go.Scatter(x=list(range(len(lag_acf))), y=lag_acf, mode='lines+markers'))
    fig_acf.update_layout(title=f'Autocorrelation of {option_slctd}',
                          template='plotly_dark')

    fig_pacf = go.Figure()
    fig_pacf.add_trace(go.Scatter(x=list(range(len(lag_pacf))), y=lag_pacf, mode='lines+markers'))
    fig_pacf.update_layout(title=f'Partial Autocorrelation of {option_slctd}',
                           template='plotly_dark')

    return container, fig_acf, fig_pacf

@app.callback(
    [Output(component_id='output_container_N', component_property='children'),
     Output(component_id='cluster_symbol', component_property='figure')],
    [Input(component_id='slct_N', component_property='value')]
)

def cluster_markets(N):

    container =  'The cluster size chosen by the user is: {}'.format(N)

    eur=get_ohlc('EURUSD')
    eur['1d_vol']=eur['Close'].pct_change().rolling(7).std()
    gbp=get_ohlc('GBPUSD')
    gbp['1d_vol']=eur['Close'].pct_change().rolling(7).std()
    gold=get_ohlc('GOLD')
    gold['1d_vol']=eur['Close'].pct_change().rolling(7).std()
    cad=get_ohlc('USDCAD')
    cad['1d_vol']=eur['Close'].pct_change().rolling(7).std()
    jpy=get_ohlc('USDJPY')
    jpy['1d_vol']=eur['Close'].pct_change().rolling(7).std()
    chf=get_ohlc('USDCHF')
    chf['1d_vol']=eur['Close'].pct_change().rolling(7).std()

    # Assuming each dataframe has identical columns
    dfs = [eur, gbp, gold, cad, jpy, chf]
    names = ['EURUSD', 'GBPUSD', 'GOLD', 'USDCAD', 'USDJPY', 'USDCHF']

    for df, name in zip(dfs, names):
        df.columns = pd.MultiIndex.from_product([[name], df.columns])
        
    df = pd.concat(dfs, axis=1)

    # List of columns to drop NaN values from
    cols_to_check = ['High', 'Low', '1d_vol']

    # Iterate through each symbol
    for name in names:  
        # Drop rows where any of the specified columns have NaN values for the current symbol
        df.dropna(subset=[(name, col) for col in cols_to_check], inplace=True)

    # Initialize an empty DataFrame to store mean values for clustering
    df_means = pd.DataFrame(columns=['Mean_High', 'Mean_Low', 'Mean_1d_vol'], index=names)

    # Calculate the mean values for 'High', 'Low', and '1d_vol' for each instrument
    for name in names:
        df_means.loc[name, 'Mean_High'] = df[(name, 'High')].mean()
        df_means.loc[name, 'Mean_Low'] = df[(name, 'Low')].mean()
        df_means.loc[name, 'Mean_1d_vol'] = df[(name, '1d_vol')].mean()

    # Perform clustering on the mean values
    std_scaler = StandardScaler()
    cluster_data = std_scaler.fit_transform(df_means)
    km = KMeans(random_state=42, n_init=10, max_iter=100, n_clusters=N)
    km.fit(cluster_data)
    df_means['label'] = km.labels_

    # Create 3D scatter plot using mean values but colored by the cluster label
    fig = px.scatter_3d(df_means,
                        x='Mean_High',
                        y='Mean_Low',
                        z='Mean_1d_vol',
                        color='label',
                        template='plotly_dark',
                        title='Clusters of Markets',
                        labels={'label': 'Cluster Label', 'Mean_High': 'High', 'Mean_Low' : 'Low', 'Mean_1d_vol' : 'Daily Volatility'},
                        text=df_means.index)

    # Show the market names when hovering
    fig.update_traces(textposition='top center', textfont_size=12)

    
    # Adding text annotations to act as an extended legend
    for label in df_means['label'].unique():
        markets_in_cluster = ', '.join(df_means[df_means['label'] == label].index.tolist())
        annotation_text = f"Cluster {label}: {markets_in_cluster}"
        
        # Add each annotation; you may need to adjust x and y to position correctly
        fig.add_annotation(
            x=0.9,
            y=0.9 - (0.1 * label),
            xref="paper",
            yref="paper",
            text=annotation_text,
            showarrow=False,
            font=dict(
                family="Courier New, monospace",
                size=12,
                color="#ffffff"
                ),
            align="left",
            ax=0,
            ay=0,
            bordercolor="#c7c7c7",
            borderwidth=1,
            bgcolor="#ff7f0e",  # or whatever the cluster color is
        )
    
    return container, fig

if __name__ == '__main__':
    app.run_server(debug=True)

    
