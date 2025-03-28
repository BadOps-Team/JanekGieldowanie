import random
from collections import defaultdict
from typing import Self
import numpy as np

class PDF:
    def __init__(self, points: list[float]):
        self.function = [point/sum(points) for point in points]

    def __call__(self):
        return np.random.choice(np.linspace(0, 1, 1000), p=self.function)

    def uniform() -> Self:
        return PDF(np.ones(1000))

class Agent:
    def __init__(self, asset, minimum_holding_period, probability_distribution=PDF.uniform(), max_loss=0.2, strategy='basic',
                 minimum_bought=5, stop_loss=0.9, take_profit=1.2):
        self.START_ASSET = asset  # const
        self.curr_asset = asset
        self.probability_distribution = probability_distribution
        self.max_loss = max_loss
        self.profit = 0
        self.minimum_holding_period = minimum_holding_period
        self.bought = defaultdict(list)
        self.strategy = strategy
        self.minimum_bought = minimum_bought
        self.stop_loss = stop_loss
        self.take_profit = take_profit

    def make_decision(self, current_prices: dict, day: int) -> dict:
        decisions = {}


        while sum(len(v) for v in self.bought.values()) < self.minimum_bought:
            ticker = random.choice(list(current_prices.keys())) # gamblujemy decyzje es
            if self.curr_asset >= current_prices[ticker] and self.probability_distribution() < 0.5:
                decisions[ticker] = {'action': 'buy', 'quantity': 1} # quantity?
                break

        for ticker, transactions in list(self.bought.items()):
            for txn in transactions:
                buy_price = txn['price']
                if day - txn['day'] >= self.minimum_holding_period:
                    if current_prices[ticker] <= buy_price * self.stop_loss and self.probability_distribution() < 0.7:
                        decisions[ticker] = {'action': 'sell', 'quantity': txn['quantity']}
                    elif current_prices[ticker] >= buy_price * self.take_profit and self.probability_distribution() < 0.8:
                        decisions[ticker] = {'action': 'sell', 'quantity': txn['quantity']}

        return decisions

    def execute_transaction(self, ticker: str, decision: dict, price: float, day: int) -> dict or None:
        if decision['action'] == 'buy':
            total_cost = price * decision['quantity']
            if self.curr_asset >= total_cost:
                self.curr_asset -= total_cost
                self.bought[ticker].append({'day': day, 'price': price, 'quantity': decision['quantity']})
                return {'ticker': ticker, 'action': 'buy', 'price': price, 'quantity': decision['quantity']}

        elif decision['action'] == 'sell':
            if self.bought[ticker]:
                txn = self.bought[ticker].pop(0)  # najstarsza akcja
                self.curr_asset += price * txn['quantity']
                self.profit += txn['quantity'] * (price - txn['price'])
                return {'ticker': ticker, 'action': 'sell', 'price': price, 'quantity': txn['quantity']}

        return None

    def get_total_profit(self) -> float:
        return self.profit

    def check_loss(self) -> bool:
        return self.profit < -self.max_loss * self.START_ASSET