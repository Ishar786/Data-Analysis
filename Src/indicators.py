import pandas as pd
import numpy as np

def moving_average(df: pd.DataFrame, price_col = 'Close', windows = [20, 50, 200]) -> pd.DataFrame:
    for w in windows:
        df[f'MA_{w}'] = df['Close'].rolling(window=w).mean()
    return df

def bolllinger_bands(df: pd.DataFrame, price_col = 'Close', window: int = 20, num_std: int = 2) -> pd.DataFrame:
    rolling_mean = df[price_col].rolling(window=window).mean()
    rolling_std = df[price_col].rolling(window=window).std()
    df['Bollinger_Upper'] = rolling_mean + (rolling_std * num_std)
    df['Bollinger_Lower'] = rolling_mean - (rolling_std * num_std)
    return df

def macd(df, price_col='Close', span_short=12, span_long=26, span_signal=9):
    ema_short = df[price_col].ewm(span=span_short, adjust=False).mean()
    ema_long = df[price_col].ewm(span=span_long, adjust=False).mean()
    df['MACD'] = ema_short - ema_long
    df['MACD_Signal'] = df['MACD'].ewm(span=span_signal, adjust=False).mean()
    return df

def rsi(df, price_col='Close', period=14):
    delta = df[price_col].diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    # Wilder smoothing using exponential moving average with alpha = 1/period
    ma_up = up.ewm(alpha=1/period, adjust=False).mean()
    ma_down = down.ewm(alpha=1/period, adjust=False).mean()
    rs = ma_up / ma_down
    df['RSI'] = 100 - (100 / (1 + rs))
    return df