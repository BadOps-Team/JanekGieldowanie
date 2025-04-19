from Stocks.period import Period
from Stocks.stock_utility import StockUtility

class Market:
    def __init__(self, ticker : str, period : Period):
        self.ticker = ticker
        self.period = period
        self.data = StockUtility(ticker).get_historical_data(period)['Close'].to_list()
