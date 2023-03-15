import pandas as pd
import os
from predict import predict_closing

# Load list of S&P tickers
ticker_files = [f for f in os.listdir('historical_data') if f.endswith('.csv')]

# Initialize portfolio balance and portfolio history list
balance = 1000
history = []

# Set start and end dates for simulation
start_date = '2022-10-10'
end_date = '2022-10-13'

# Initialize currently held ticker
held_ticker = None
not_day_one = False
# Loop through each day of the simulation
date = start_date
while date <= end_date:

        ticker_profits = []
        for ticker_file in ticker_files:
            result = predict_closing(ticker_file, date)
            if result:
                ticker, profit_loss, profit_percent = result
                ticker_profits.append((ticker, profit_percent))
        
        ticker_profits.sort(key=lambda x: x[1], reverse=True)       
        
        #Price of Yesterdays Ticker -> Actual Result
        df = pd.read_csv(f'historical_data/{most_profitable_ticker}.csv')
        last_closing_price = df[df['Date'] == next_date]['Close'].iloc[0]
        print(f"{date}: {most_profitable_ticker} {last_closing_price}")

        ticker_profits = []
        for ticker_file in ticker_files:
            result = predict_closing(ticker_file, next_date)
            if result:
                ticker, profit_loss, profit_percent = result
                ticker_profits.append((ticker, profit_percent))
        
        ticker_profits.sort(key=lambda x: x[1], reverse=True)
        
        #Predicted price of tommorow's closing
        predicted_most_profitable_ticker = ticker_profits[0][0]
        df = pd.read_csv(f'historical_data/{predicted_most_profitable_ticker}.csv')
        last_closing_price = df[df['Date'] == next_date]['Close'].iloc[0]
        print(f"{date}: {predicted_most_profitable_ticker} {last_closing_price}")
     
 
        date = pd.to_datetime(date) + pd.Timedelta(days=1)
        date = date.strftime('%Y-%m-%d')

        

 
