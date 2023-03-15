import requests
import json
import pandas as pd
import os

# Replace YOUR_API_KEY with your Alpha Vantage API key
API_KEY = os.environ.get('ALPHA_API_KEY')

# Get the list of S&P 500 tickers
sp_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()

# Check if 'intraday_data' folder exists, and create it if it doesn't
if not os.path.exists('intraday_data'):
    os.mkdir('intraday_data')

# Define start and end times for the intraday data
start_time = "09:00:00"
end_time = "14:00:00"

# Loop through the S&P 500 tickers
for symbol in sp_tickers:
    # Make an API call to get the stock data
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=60min&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    try:
        # Create a DataFrame to store the intraday data
        df = pd.DataFrame(columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume'])

        # Loop through the intraday data and add each hour's data to the DataFrame
        for key in data["Time Series (60min)"]:
            row = [key, data["Time Series (60min)"][key]["1. open"], data["Time Series (60min)"][key]["2. high"], 
                   data["Time Series (60min)"][key]["3. low"], data["Time Series (60min)"][key]["4. close"], 
                   data["Time Series (60min)"][key]["5. volume"]]
            df.loc[len(df)] = row

        # Save the intraday data to a CSV file
        file_path = f"intraday_data/{symbol}.csv"
        df.to_csv(file_path, index=False)

        print(f"Saved intraday data for {symbol} to {file_path}")
    
    except KeyError:
        print(f"No data found for {symbol}")
        continue

