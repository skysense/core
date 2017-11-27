import pandas as pd


def compute_returns(close_prices):
    returns = pd.DataFrame(close_prices)
    returns.columns = ['prices']
    returns['prices shift'] = close_prices.shift(1)
    returns['returns'] = (returns['prices'] / returns['prices shift'] - 1) * 100  # percentage.
    returns.fillna(0.0, inplace=True)
    return returns['returns']
