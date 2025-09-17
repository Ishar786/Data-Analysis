import yfinance as yf
import pandas as pd
from typing import Optional

def get_stock_data(ticker_symbol: str, period: str = "1y", interval: str = "1d") -> Optional[pd.DataFrame]:
    if not ticker_symbol:
        raise ValueError("Ticker symbol must be provided.")
    df = yf.download(ticker_symbol, period=period, interval=interval)
    if df.empty:
        raise ValueError(f"No data found for ticker symbol: {ticker_symbol}")
    df.index = pd.to_datetime(df.index)
    df = df.sort_index(ascending=False).tz_localize(None)
    return df

def validate_and_fill(df,method: Optional[str]) -> pd.DataFrame:
    if df.isna().sum().sum() > 0:
        if method == "ffill":
            df = df.fillna(method="ffill")
        elif method == "bfill":
            df = df.fillna(method="bfill")
    return df


