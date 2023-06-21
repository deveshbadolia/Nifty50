import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date
import matplotlib.pyplot as plt
import statistics

# Set Streamlit page configuration
st.set_page_config(layout='wide')
st.set_option('deprecation.showPyplotGlobalUse', False)

# Display header
st.header("National Stock Exchange - Nifty 50")

# Define column layout
c1, c2, c3, c4, c5 = st.columns(5)

# Get user inputs
with c1:
    sim_start_date = st.date_input("Enter the Simulation Date", date(2020, 10, 1))
with c2:
    end_date = st.date_input("Enter the End Date", date.today())
with c3:
    days = st.slider("Number of Days for Performance", 1, 200, value=100)
with c4:
    top_n_stocks = st.number_input('Top Stocks', 0, 10, value=5)
with c5:
    int_eq = st.number_input("Enter the initial equity", 1000000, 20000000)

# Define benchmark strategy
def benchmark_strategy():
    # Stock symbols for benchmark strategy
    stock = ['ADANIPORTS.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 'BHARTIARTL.NS', 'BPCL.NS', 'BRITANNIA.NS', 'CIPLA.NS',
             'COALINDIA.NS', 'DIVISLAB.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFC.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS',
             'HINDUNILVR.NS', 'ICICIBANK.NS', 'INDUSINDBK.NS', 'INFY.NS', 'IOC.NS', 'ITC.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LT.NS', 'M&M.NS', 'MARUTI.NS', 'NESTLEIND.NS',
             'NTPC.NS', 'ONGC.NS', 'POWERGRID.NS', 'RELIANCE.NS', 'SBILIFE.NS', 'SBIN.NS', 'SHREECEM.NS', 'SUNPHARMA.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATASTEEL.NS',
             'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'ULTRACEMCO.NS', 'UPL.NS', 'WIPRO.NS']

    # Download stock data
    data = yf.download(stock, start=sim_start_date, end=end_date)["Close"]

    # Normalize data
    normalized_data = data.div(data.iloc[0])

    # Calculate position size
    num_stocks = len(stock)
    position_size = int_eq / num_stocks

    # Calculate stock values
    stock_values = normalized_data * position_size

    # Calculate equity curve
    equity_curve = stock_values.sum(axis=1)

    # Calculate daily returns
    daily_returns = equity_curve.pct_change()

    # Calculate volatility
    volatility = (pow(daily_returns.std(), (1 / 252))) * 100

    # Calculate CAGR
    vfinal = equity_curve.iloc[-1]
    vbegin = equity_curve.iloc[0]
    number_of_years = (date.today() - sim_start_date).days / 365
    CAGR = ((vfinal / vbegin) ** (1 / number_of_years) - 1) * 100

    # Calculate Sharpe ratio
    sharpe_ratio = (statistics.mean(daily_returns) / daily_returns.std()) ** (1 / 252)

    return equity_curve, volatility, CAGR, sharpe_ratio

# Define sample strategy
def sample_strategy():
    # Stock symbols for sample strategy
    stock = ['ADANIPORTS.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS',
             'BHARTIARTL.NS', 'BPCL.NS', 'BRITANNIA.NS', 'CIPLA.NS',
             'COALINDIA.NS', 'DIVISLAB.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFC.NS',
             'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS',
             'HINDUNILVR.NS', 'ICICIBANK.NS', 'INDUSINDBK.NS', 'INFY.NS', 'IOC.NS', 'ITC.NS', 'JSWSTEEL.NS',
             'KOTAKBANK.NS', 'LT.NS', 'M&M.NS', 'MARUTI.NS', 'NESTLEIND.NS',
             'NTPC.NS', 'ONGC.NS', 'POWERGRID.NS', 'RELIANCE.NS', 'SBILIFE.NS', 'SBIN.NS', 'SHREECEM.NS',
             'SUNPHARMA.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATASTEEL.NS',
             'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'ULTRACEMCO.NS', 'UPL.NS', 'WIPRO.NS']
    stock = [stock[i] for i in range(0, top_n_stocks)]

    # Download stock data
    df = yf.download(stock, start=sim_start_date, end=end_date)["Close"]

    # Extract latest 100 days data
    latest_100_days = df.iloc[-days:-1]

    # Calculate returns and cumulative returns
    returns = latest_100_days.pct_change().iloc[1:]
    cumulative_returns = returns.cumsum()

    # Normalize data
    normalized_data = df.div(df.iloc[0])

    # Calculate position size
    position_size = int_eq / top_n_stocks

    # Calculate stock values
    stock_values = normalized_data * position_size

    # Calculate portfolio equity curve
    portfolio_equity_curve = stock_values.sum(axis=1)

    # Calculate daily returns
    daily_returns = portfolio_equity_curve.pct_change()

    # Calculate volatility
    volatility = (pow(daily_returns.std(), (1 / 252))) * 100

    # Calculate CAGR
    vfinal = portfolio_equity_curve.iloc[-1]
    vbegin = portfolio_equity_curve.iloc[0]
    number_of_years = (date.today() - sim_start_date).days / 365
    CAGR = ((vfinal / vbegin) ** (1 / number_of_years) - 1) * 100

    # Calculate Sharpe ratio
    sharpe_ratio = (statistics.mean(daily_returns) / daily_returns.std()) ** (1 / 252)

    return portfolio_equity_curve, volatility, CAGR, sharpe_ratio

# Define Nifty strategy
def nifty_equity():
    # Download Nifty data
    df_nifty = yf.download('^NSEI', start=sim_start_date, end=end_date)['Close']

    # Normalize data
    normalized_data = df_nifty.div(df_nifty.iloc[0])

    # Calculate position size
    position_size = int_eq

    # Calculate stock values
    stock_values = normalized_data * position_size

    # Calculate daily returns
    daily_returns = stock_values.pct_change()

    # Calculate volatility
    volatility = (pow(daily_returns.std(), (1 / 252))) * 100

    # Calculate CAGR
    vfinal = stock_values.iloc[-1]
    vbegin = stock_values.iloc[0]
    number_of_years = (date.today() - sim_start_date).days / 365
    CAGR = ((vfinal / vbegin) ** (1 / number_of_years) - 1) * 100

    # Calculate Sharpe ratio
    sharpe_ratio = (statistics.mean(daily_returns) / daily_returns.std()) ** (1 / 252)

    return stock_values, volatility, CAGR, sharpe_ratio

# Calculate equity curve and performance metrics for each strategy
sample_equity, sample_volatility, sample_CAGR, sample_sharpe_ratio = sample_strategy()
nifty_equity_curve, nifty_volatility, nifty_CAGR, nifty_sharpe = nifty_equity()
benchmark_equity, benchmark_volatility, benchmark_CAGR, benchmark_sharpe_ratio = benchmark_strategy()

# Plot equity curves
plt.figure(figsize=(9, 3))
plt.plot(benchmark_equity, label='Benchmark strategy')
plt.plot(nifty_equity_curve, label='Nifty')
plt.plot(sample_equity, label='Sample strategy')
plt.xlabel("Date")
plt.ylabel("Equity")
plt.legend()
st.pyplot()

# Display performance metrics in a DataFrame
data = {'Index': ['Sample strategy', 'Nifty', 'Benchmark strategy'],
        'CAGR %': [sample_CAGR, nifty_CAGR, benchmark_CAGR],
        'Volatility %': [sample_volatility, nifty_volatility, benchmark_volatility],
        'Sharpe Ratio': [sample_sharpe_ratio, nifty_sharpe, benchmark_sharpe_ratio]}

# Display DataFrame
st.dataframe(data, hide_index=True)
