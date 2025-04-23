import random
from collections import defaultdict
import numpy as np

class Agent:
    def __init__(self, asset, minimum_holding_period, probability_distribution=lambda: random.uniform(0, 1), max_loss=0.2, strategy='basic',
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

    # estimated prices postaci {"TICKER1": [array_of_prices],
    #                          {"TICKER2": [array]...}
    # current prices podobnie, {"TICKER1": current_price,
    #                          {"TICKER2": current_price...}
    def make_decision(self, current_prices: dict, estimated_prices: dict, day: int) -> dict:
        decisions = {}

        for ticker, future_prices in estimated_prices.items():
            if not future_prices:
                continue

            current_estimated_price = current_prices[ticker]
            max_future_price = max(future_prices)

            # jesli potencjalny zysk spelnia nasze oczekiwania, to kupujemy
            if max_future_price >= current_estimated_price * self.take_profit:
                quantity = 1
                total_cost = current_estimated_price * quantity
                if self.curr_asset >= total_cost and self.probability_distribution() < 0.8:
                    decisions[ticker] = {'action': 'buy', 'quantity': quantity}

        for ticker, transactions in list(self.bought.items()):
            if not estimated_prices.get(ticker):
                continue
            current_estimated_price = current_prices[ticker]
            min_future_price = min(estimated_prices[ticker])
            max_future_price = max(estimated_prices[ticker])

            for txn in transactions:
                buy_price = txn['price']
                if day - txn['day'] >= self.minimum_holding_period:
                    # jesli spodziewamy sie duzej straty, sprzedajemy
                    if min_future_price <= buy_price * self.stop_loss and self.probability_distribution() < 0.7:
                        decisions[ticker] = {'action': 'sell', 'quantity': txn['quantity']}
                    # sprawdzamy, czy juz zarobilismy ile chcielismy oraz czy nie oplaca sie czekac jeszcze chwile
                    elif current_estimated_price >= buy_price * self.take_profit and current_estimated_price > max_future_price and self.probability_distribution() < 0.8:
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