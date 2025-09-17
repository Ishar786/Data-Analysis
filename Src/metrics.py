import numpy as np
import pandas as pd

TRADING_DAYS = 252

def cumulative_return_metric(df, price_col='Close'):
    start = df[price_col].iloc[0]
    end = df[price_col].iloc[-1]
    return (end / start) - 1

def cummulative_return(df: pd.DataFrame) -> pd.DataFrame:
    df['Cumulative Return'] = (1 + df['Daily Return']).cumprod() - 1
    return df


def cagr(df, price_col='Close'):
    start = df[price_col].iloc[0]
    end = df[price_col].iloc[-1]
    days = (df.index[-1] - df.index[0]).days
    years = days / 365.25
    return (end / start) ** (1 / years) - 1

def annualized_volatility(df, return_col='Daily Return'):
    return df[return_col].std() * np.sqrt(TRADING_DAYS)


def sharpe_ratio(df, rf=0.0, return_col='Daily Return'):
    # rf: risk-free rate as annual decimal (e.g., 0.03)
    ann_ret = df[return_col].mean() * TRADING_DAYS
    ann_vol = df[return_col].std() * np.sqrt(TRADING_DAYS)
    if ann_vol == 0:
        return np.nan
    return (ann_ret - rf) / ann_vol

def max_drawdown(df, price_col='Close'):
    cum = df[price_col] / df[price_col].iloc[0]
    running_max = cum.cummax()
    drawdown = cum / running_max - 1
    return drawdown.min()  # negative value


def sma_crossover_backtest(df, short=20, long=50):
    df = df.copy()
    df[f"SMA_{short}"] = df['Close'].rolling(window=short).mean()
    df[f"SMA_{long}"] = df['Close'].rolling(window=long).mean()
    df['signal'] = 0
    df.loc[df[f"SMA_{short}"] > df[f"SMA_{long}"], 'signal'] = 1
    df['position'] = df['signal'].shift(1).fillna(0)  # trade at next bar open theoretically
    df['strategy_return'] = df['Daily Return'] * df['position']
    df['strategy_cum'] = (1 + df['strategy_return'].fillna(0)).cumprod() - 1
    df['buy_and_hold_cum'] = (1 + df['Daily Return'].fillna(0)).cumprod() - 1
    # performance summary
    perf = {
        'strategy_cumulative_return': df['strategy_cum'].iloc[-1],
        'buy_and_hold_cumulative_return': df['buy_and_hold_cum'].iloc[-1],
        'strategy_sharpe': sharpe_ratio(df.assign(**{'Daily Return': df['strategy_return']}))
    }
    return df, perf
