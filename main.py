import yfinance as yf
import plotly.graph_objs as go
import numpy as np
from sklearn.linear_model import LinearRegression


def evaluate_stock(stock_data):
    # Get the latest two closing prices
    latest_close = stock_data["Close"].iloc[-1]
    prev_close = stock_data["Close"].iloc[-2]

    # Calculate percentage change
    pct_change = ((latest_close - prev_close) / prev_close) * 100

    print("Latest Close Price:", latest_close)
    print("Previous Close Price:", prev_close)
    print("Percentage Change:", pct_change)

    # Create candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                                         open=stock_data["Open"],
                                         high=stock_data["High"],
                                         low=stock_data["Low"],
                                         close=stock_data["Close"])])

    # Perform linear regression on closing prices
    x = np.arange(len(stock_data)).reshape(-1, 1)
    y = stock_data["Close"].values.reshape(-1, 1)

    model = LinearRegression().fit(x, y)
    trend_line = model.predict(x)

    # Add linear regression trend line to the chart
    fig.add_trace(go.Scatter(x=stock_data.index,
                             y=trend_line.flatten(),
                             mode="lines",
                             name="Trend Line",
                             line=dict(color="blue", width=2)))

    # Add buy recommendation line if pct_change > 5
    if pct_change > 5:
        buy_price = latest_close * 0.98  # Buy at 2% below current price
        fig.add_shape(type="line",
                      x0=stock_data.index[-1], y0=buy_price,
                      x1=stock_data.index[0], y1=buy_price,
                      line=dict(color="green", width=2, dash="dash"))
        print("Buy! The stock price increased by more than 5%. Buy at:", buy_price)
    else:
        print("Don't Buy. The stock price change is not significant.")

    fig.update_layout(title=f"Stock Candlestick Chart with Linear Regression",
                      xaxis_title="Date",
                      yaxis_title="Price")
    fig.show()


def main():
    # Get user input for stock symbol
    symbol = input("Enter the stock symbol (e.g., AAPL): ").upper()

    # Get stock data from Yahoo Finance
    stock = yf.Ticker(symbol)
    stock_data = stock.history(period="1mo")  # Fetching data for the last month

    if not stock_data.empty:
        # Evaluate the stock and plot candlestick chart with linear regression
        evaluate_stock(stock_data)
    else:
        print("Unable to fetch data for symbol:", symbol)


if __name__ == "__main__":
    main()
