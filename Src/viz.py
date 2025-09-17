import numpy as np
import pandas as pd

def add_basic_returns(df: pd.DataFrame) -> pd.DataFrame:
    price = df['Close'].copy()
    df['Daily Return'] = price.pct_change()
    df['Log Return'] = np.log(price / price.shift(1))
    return df

def cummulative_return(df: pd.DataFrame) -> pd.DataFrame:
    df['Cumulative Return'] = (1 + df['Daily Return']).cumprod() - 1
    return df