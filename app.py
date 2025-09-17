# app.py
import streamlit as st
import pandas as pd
from Src.data import get_stock_data
from Src.indicators import moving_average, bolllinger_bands, macd, rsi
from Src.metrics import cumulative_return_metric, cummulative_return, cagr, annualized_volatility, sharpe_ratio, max_drawdown, sma_crossover_backtest
from Src.viz import add_basic_returns, cummulative_return

st.set_page_config(layout="wide", page_title="Stock EDA Dashboard")

st.title("📈 Stock EDA & Dashboard")

with st.sidebar:
    ticker = st.text_input("Ticker", value="AAPL")
    period = st.selectbox("period", options=["1y","2y","3y"])
    interval = st.selectbox("Interval", options=["1d","1wk","1mo"])
    run = st.button("Load")

@st.cache_data(ttl=3600)
def load_data(ticker, period, interval):
    return get_stock_data(ticker, period = period, interval=interval)

if run:
    try:
        df = load_data(ticker, period, interval)
        # Add return columns
        df = add_basic_returns(df)
        df = cummulative_return(df)  # column for plotting
        
        # Indicators
        df = moving_average(df)
        df = bolllinger_bands(df)
        df = macd(df)
        df = rsi(df)
        
        # KPIs
        st.subheader("KPIs")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Cumulative Return", f"{cumulative_return_metric(df):.2%}")
        col2.metric("CAGR", f"{cagr(df):.2%}")
        col3.metric("Sharpe", f"{sharpe_ratio(df):.2f}")
        col4.metric("Latest Price", f"{df['Close'].iloc[-1]:.2f}")
        
        # Price + MA chart
        st.subheader("Price + MAs")
        st.line_chart(df[['Close','MA_20','MA_50','MA_200']].dropna())
        
        # SMA Crossover Backtest
        st.subheader("SMA Crossover Backtest (20/50)")
        bt_df, perf = sma_crossover_backtest(df)
        st.write(perf)
        st.line_chart(pd.DataFrame({
            'Strategy': bt_df['strategy_cum'],
            'Buy & Hold': bt_df['buy_and_hold_cum']
        }).dropna())
        
    except Exception as e:
        st.error(str(e))
