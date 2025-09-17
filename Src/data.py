import yfinance as yf
import pandas as pd
from typing import Optional

def get_stock_data(ticker_symbol: str, period: str = "1y", interval: str = "1d") -> Optional[pd.DataFrame]:
    if not ticker_symbol:
        raise ValueError("Ticker symbol must be provided.")
    df = yf.download(ticker_symbol, period=period, interval=interval, progress=False)
    if df.empty:
        raise ValueError(f"No data found for ticker symbol: {ticker_symbol}")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]
    df.index = pd.to_datetime(df.index)
    df = df.sort_index(ascending=True).tz_localize(None)
    if "Close" not in df.columns:
        df["Close"] = df["Close"]
    return df

def validate_and_fill(df,method: Optional[str]) -> pd.DataFrame:
    if df.isna().sum().sum() > 0:
        if method == "ffill":
            df = df.fillna(method="ffill")
        elif method == "bfill":
            df = df.fillna(method="bfill")
    return df



