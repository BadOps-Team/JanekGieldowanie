from typing import List
from Simulation.market import Market
from Stocks.period import Period
from Simulation.exceptions import InconsistentTickerDataSize

class MarketCollection:
    def __init__(self, ticker_names : List[str], period : Period):
        self.markets = [Market(ticker, period) for ticker in ticker_names]
        self.no_days = len(self.markets[0].data)
        for market in self.markets[1:]:
            if len(market.data) != self.no_days:
                raise InconsistentTickerDataSize([(m.ticker, len(m.data)) for m in self.markets])
        self.day = 0
        
    def add_market(self, market : Market):
        self.market.append(market)

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.day >= self.no_days:
            raise StopIteration
        
        prices = {}


        for market in self.markets:
            prices.update({market.ticker : market.data[self.day]})
        
        self.day += 1

        return prices