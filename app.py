# app.py
import streamlit as st
import pandas as pd
from src.data import get_stock_data
from src.indicators import moving_averages, bollinger_bands, macd, rsi
from src.metrics import add_basic_returns, cagr, sharpe_ratio, max_drawdown, sma_crossover_backtest

st.set_page_config(layout="wide", page_title="Stock EDA Dashboard")

st.title("📈 Stock EDA & Dashboard")

with st.sidebar:
    ticker = st.text_input("Ticker", value="AAPL")
    start = st.date_input("Start date", value=pd.to_datetime("2020-01-01"))
    end = st.date_input("End date", value=pd.to_datetime("today"))
    interval = st.selectbox("Interval", options=["1d","1wk","1mo"])
    run = st.button("Load")

@st.cache_data(ttl=3600)
def load_data(ticker, start, end, interval):
    return get_stock_data(ticker, start.isoformat(), end.isoformat(), interval=interval)

if run:
    try:
        df = load_data(ticker, start, end, interval)
        df = add_basic_returns(df)
        df = moving_averages(df)
        df = bollinger_bands(df)
        df = macd(df)
        df = rsi(df)
        # KPIs
        st.subheader("KPIs")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("CAGR", f"{cagr(df):.2%}")
        col2.metric("Sharpe", f"{sharpe_ratio(df):.2f}")
        col3.metric("Max Drawdown", f"{max_drawdown(df):.2%}")
        col4.metric("Latest Price", f"{df['Adj Close'].iloc[-1]:.2f}")
        # Plots (use plotly in viz.py or quick st.line_chart)
        st.subheader("Price + MAs")
        st.line_chart(df[['Adj Close','MA20','MA50','MA200']].dropna())
        # Backtest
        st.subheader("SMA Crossover Backtest (20/50)")
        bt_df, perf = sma_crossover_backtest(df)
        st.write(perf)
        st.line_chart(pd.DataFrame({
            'Strategy': bt_df['strategy_cum'],
            'Buy & Hold': bt_df['buy_and_hold_cum']
        }).dropna())
    except Exception as e:
        st.error(str(e))
