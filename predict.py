import pandas as pd
import os
from sklearn.linear_model import LinearRegression

import pandas as pd
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings("ignore")

import pickle


def predict_closing(ticker_file, date):
    # Load historical data into a Pandas dataframe
    df = pd.read_csv(f'historical_data/{ticker_file}')

    if df.empty:
        return
    
    # Extract the closing price for the given date
    date_df = df.loc[df['Date'] == date]
    if date_df.empty:
        return
    last_closing_price = date_df.iloc[0]['Close']

    # Set the features (historical price data) and target (the next day's closing price)
    X = df.drop(['Date', 'Close', 'Adj Close'], axis=1)
    y = df['Close'].shift(-1)

    # Split the data into training and testing sets
    split = int(0.8 * len(df))
    X_train, X_test, y_train, y_test = X[:split], X[split:], y[:split], y[split:]

    # Load pre-trained model if it exists, or train a new one if it doesn't
    if os.path.exists('model.pkl'):
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
    else:
        model = LinearRegression()
        model.fit(X_train, y_train)
        with open('model.pkl', 'wb') as f:
            pickle.dump(model, f)

    X.columns = X_train.columns
    # Make predictions for the next two days
    next_day_data = [[last_closing_price, last_closing_price, last_closing_price, last_closing_price]]
    next_day_price = model.predict(next_day_data)[0]
    day_after_data = [[next_day_price, next_day_price, next_day_price, next_day_price]]
    day_after_price = model.predict(day_after_data)[0]

    # Calculate estimated profit/loss
    buy_price = next_day_price
    sell_price = day_after_price
    profit_loss = sell_price - buy_price
    profit_percent = profit_loss / buy_price * 100
    ticker = os.path.splitext(os.path.basename(ticker_file))[0]
    # Print the results
    # Check if expected profit is positive
    if profit_loss > 0.01:
        return ticker, profit_loss, profit_percent


