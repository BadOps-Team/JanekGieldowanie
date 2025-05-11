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
        self.stop_loss = 0
        self.take_profit = 0
        self.set_strategy_thresholds()

    def set_strategy_thresholds(self):
        if self.strategy == 'basic':
            self.stop_loss = 0.9
            self.take_profit = 1.2
        elif self.strategy == 'risky':
            self.stop_loss = 0.8
            self.take_profit = 1.4
        elif self.strategy == 'soft':
            self.stop_loss = 0.95
            self.take_profit = 1.1

    # estimated prices postaci {"TICKER1": [array_of_prices],
    #                          {"TICKER2": [array]...}
    # current prices podobnie, {"TICKER1": current_price,
    #                          {"TICKER2": current_price...}
    def make_decision(self, current_prices: dict, estimated_prices: dict, day: int) -> dict:
        decisions = {}

        for ticker, future_prices in estimated_prices.items():
            if future_prices is None or len(future_prices) == 0:
                continue

            current = current_prices[ticker]
            max_future = max(future_prices)
            threshold = current * self.take_profit


            if max_future >= threshold:
                quantity = 1
                cost = current * quantity
                prob = self.probability_distribution()
                if self.curr_asset >= cost and prob < 0.8:
                    decisions[ticker] = {'action': 'buy', 'quantity': quantity}


        for ticker, transactions in list(self.bought.items()):
            if ticker not in estimated_prices or estimated_prices[ticker] is None:
                continue

            current = current_prices[ticker]
            min_future = min(estimated_prices[ticker])
            max_future = max(estimated_prices[ticker])

            for txn in transactions:
                buy_price = txn['price']
                held = day - txn['day'] >= self.minimum_holding_period

                if not held:
                    continue


                prob = self.probability_distribution()
                # stop-loss
                if min_future <= buy_price * self.stop_loss and prob < 0.7:
                    decisions[ticker] = {'action': 'sell', 'quantity': txn['quantity']}
                # take-profit
                elif current >= buy_price * self.take_profit and current > max_future and prob < 0.8:
                    decisions[ticker] = {'action': 'sell', 'quantity': txn['quantity']}

        return decisions

    def execute_transaction(self, ticker: str, decision: dict, price: float, day: int) -> dict:
        if decision['action'] == 'buy':
            total_cost = price * decision['quantity']
            if self.curr_asset >= total_cost:
                self.curr_asset -= total_cost
                self.bought[ticker].append({'day': day, 'price': price, 'quantity': decision['quantity']})
                return {'ticker': ticker, 'action': 'buy', 'price': price, 'quantity': decision['quantity']}
            else:
                raise ValueError("Not enough assets to buy the requested quantity")

        elif decision['action'] == 'sell':
            if self.bought[ticker]:
                txn = self.bought[ticker].pop(0)  # najstarsza akcja
                self.curr_asset += price * txn['quantity']
                self.profit += txn['quantity'] * (price - txn['price'])
                return {'ticker': ticker, 'action': 'sell', 'price': price, 'quantity': txn['quantity']}

        raise ValueError("Invalid decision")

    def get_total_profit(self) -> float:
        return self.profit

    # gdy utracimy juz dane startowe pieniadze, przerywamy gre
    def check_loss(self) -> bool:
        return self.profit < -self.max_loss * self.START_ASSET