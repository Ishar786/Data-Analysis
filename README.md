# Data-Analysis

# Stock EDA & Dashboard

A Python project that fetches stock data using **yfinance, performs **exploratory data analysis (EDA)**, calculates key **financial metrics**, technical indicators, and provides a **Streamlit dashboard** for interactive visualization and decision making.

---

## Features

- Fetch historical stock data (`1d`, `1wk`, `1mo`) for multiple periods (`1y`, `2y`, `3y`) using `yfinance`.
- Compute **Daily Return**, **Log Return**, and **Cumulative Return**.
- Calculate key **financial KPIs**:
  - Cumulative Return
  - CAGR (Compound Annual Growth Rate)
  - Sharpe Ratio
  - Max Drawdown
  - Latest Price
- Technical indicators:
  - Moving Averages (20, 50, 200 days)
  - Bollinger Bands
  - MACD
  - RSI
- SMA Crossover Backtest (20/50) with performance metrics.
- Interactive visualization with **Streamlit**:
  - Price chart with moving averages
  - Cumulative return chart
  - Backtesting strategy vs Buy & Hold

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Ishar786/Data-Analysis.git
cd stock-eda-dashboard
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Usage
Run the Streamlit app:

bash
Copy code
streamlit run app.py
Open the URL provided in the terminal (usually http://localhost:8501).

In the sidebar:

Enter the ticker symbol (e.g., AAPL, MSFT).

Select the period and interval.

Click Load to fetch and visualize the data.

File Structure
bash
Copy code
├── Src/
│   ├── data.py           # Fetch stock data
│   ├── indicators.py     # Technical indicators
│   ├── metrics.py        # Financial metrics and backtest functions
│   └── viz.py            # Optional visualization helper functions
├── app.py                # Streamlit dashboard
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation

Key Notes

Ensure the dataframe is sorted by ascending date for correct computation of returns and cumulative metrics.

Daily return and cumulative return are critical for strategy backtesting.

The app can be extended with:

More technical indicators (e.g., EMA, Stochastic Oscillator)

Interactive charts using Plotly

Multiple stock comparison

References
yfinance Documentation

Streamlit Documentation

Investopedia: Key Stock Metrics

Author
Your Sheik Ishar
Email: isharsheik33863@gmail.com
