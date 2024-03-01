import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from ta.trend import SMAIndicator   # You might need to install 'ta' library

# Title and Layout
st.title("Stock Analysis App")
st.sidebar.header("User Input")

# Function to fetch stock data
def get_stock_data(ticker, period):
    data = yf.download(ticker, period=period)
    data.reset_index(inplace=True)
    return data

# Function to calculate indicators
def calculate_indicators(df):
    df['SMA_20'] = SMAIndicator(df['Close'], window=20).sma_indicator()
    df['SMA_50'] = SMAIndicator(df['Close'], window=50).sma_indicator()
    df['SMA_200'] = SMAIndicator(df['Close'], window=200).sma_indicator()
    return df

# Function to create the candlestick chart
def create_candlestick_chart(df):
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'])
    ])

    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_20'], mode='lines', name='SMA 20', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_50'], mode='lines', name='SMA 50', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_200'], mode='lines', name='SMA 200', line=dict(color='black')))

    fig.add_bar(x=df['Date'], y=df['Volume'], name='Volume', yaxis='y2')

    fig.update_layout(
        yaxis=dict(title='Price'),
        yaxis2=dict(title='Volume', overlaying='y', side='right'),
        xaxis=dict(rangeslider=dict(visible=False))
    )

    return fig

# Function to create RSI chart (add RSI calculation as needed)
def create_rsi_chart(df):
    # ... Implement RSI calculation here ...
    fig = go.Figure(data=[go.Scatter(x=df['Date'], y=df['RSI'])])
    return fig

# --- App Interface ---
ticker = st.sidebar.text_input("Stock Ticker", 'AAPL')
period = st.sidebar.selectbox("Period", ['1wk', '1mo', '6mo', '1y', '3y', 'all'])
show_rsi = st.sidebar.checkbox("Show RSI")

# Get data and calculate indicators
data = get_stock_data(ticker, period)
data = calculate_indicators(data)

# Display the main candlestick/volume chart
st.plotly_chart(create_candlestick_chart(data))

# Display the RSI chart if the option is selected
if show_rsi:
    st.plotly_chart(create_rsi_chart(data))
