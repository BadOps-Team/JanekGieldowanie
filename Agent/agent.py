import random
from collections import defaultdict
import numpy as np

class Agent:
    def __init__(self, asset, minimum_holding_period, probability_distribution=lambda: random.uniform(0, 1), max_loss=0.2, strategy='basic',
                 minimum_bought=5, stop_loss=0.9, take_profit=1.2, history_length = 10):
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
        self.history_length = history_length
        self.history_prices = defaultdict(list)

    def update_history(self, current_prices: dict):
        for ticker, price in current_prices.items():
            self.history_prices[ticker].append(price)
            if len(self.history_prices[ticker]) > self.history_length:
                self.history_prices[ticker].pop(0)

    @staticmethod
    def calculate_eigenvalues(sigma): # musi być macierz kwadratowa!!!
        return np.linalg.eigvalsh(sigma)

    def create_sigma_matrix(self):
        sigma = []
        for i, (ticker, prices) in enumerate(self.history_prices):
            sigma.append(prices)
            if len(prices) < self.history_length:
                for _ in range(self.history_length - len(prices)):
                    sigma[i].append(0)

        for _ in range(self.history_length - len(sigma)):
            sigma.append(np.zeros(self.history_length))

        return sigma

    def calculate_F(self, X_prime: list):
        t = len(X_prime)
        if t == 0:
            return 0
        return np.sum(X_prime) / np.sqrt(t)

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