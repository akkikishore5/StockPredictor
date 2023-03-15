import yfinance as yf
from datetime import datetime, timedelta

# Calculate start and end dates for past year
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

# Get historical data for AAPL from Yahoo Finance for past year
symbol = "AAPL"
ticker = yf.Ticker(symbol)
history = ticker.history(start=start_date, end=end_date)

# Calculate number of times AAPL closed higher than previous day's close
num_higher = 0
for i in range(1, len(history)):
    if history['Close'][i] > history['Close'][i-1]:
        num_higher += 1

# Print result
print(f"{symbol} closed higher than the previous day's close {num_higher} times over the past year.")
