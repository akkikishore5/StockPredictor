import pandas as pd
import os
from predict import predict_closing

# Load list of S&P tickers
ticker_files = [f for f in os.listdir('historical_data') if f.endswith('.csv')]

results = []
for ticker_file in ticker_files:
    result = predict_closing(ticker_file, '2023-03-12')
    if result:
        results.append(result)

# Sort results by profit_percent in descending order
results.sort(key=lambda x: x[2])

# Print results
for result in results:
    ticker, profit_loss, profit_percent = result
    print(f"${ticker} :Estimated profit/loss: ${profit_loss:.2f} ({profit_percent:.2f}%)")

    

