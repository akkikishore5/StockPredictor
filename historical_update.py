import pandas as pd
import yfinance as yf
import os

sp_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()

# Check if 'data' folder exists, and create it if it doesn't
if not os.path.exists('historical_data'):
    os.mkdir('historical_data')

# Loop through the S&P 500 tickers
for ticker in sp_tickers:
    # Check if CSV file for the ticker already exists in the 'data' folder
    file_path = f"historical_data/{ticker}.csv"
    if os.path.exists(file_path):
        # Check if the data in the file is current (as of March 13, 2023)
        df = pd.read_csv(file_path)
        last_date = df.iloc[-1]['Date']
        if last_date == '2023-03-13':
            print(f"Skipping {ticker} as up-to-date data already exists")
            continue
    
    # Download data for the ticker if it doesn't already exist or is outdated
    print(f"Downloading data for {ticker}")
    data = yf.download(ticker, start="1970-01-01", end="2023-03-14")
    data.to_csv(file_path)
