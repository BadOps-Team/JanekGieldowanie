import random

class Agent:
    def __init__(self, asset, minimum_holding_period, probabil_distribution = lambda: random.uniform(0, 1), max_loss=20, strategy='basic', minimum_bought=5):
        self.START_ASSET = asset # const
        self.curr_asset = asset
        self.probabil_distribution = probabil_distribution
        self.max_loss = max_loss # (0-1)
        self.profit = 0
        self.minimum_holding_period = minimum_holding_period
        self.bought = {} # do trackingu, po jakiej cenie kupil i w jakim dniu, aby obliczyc profit
        self.strategy = strategy
        self.minimum_bought = minimum_bought

    def make_decision(self, current_prices: dict, day: int) -> dict:
        # gamblujemy czy kupujemy es
        while True:
            ticker = random.choice(list(current_prices.keys()))
            if ticker not in self.bought:
                break
        if self.strategy == 'basic':
            return {ticker: {'action': 'buy' if self.probabil_distribution() < 0.5 else 'sell', 'quantity': 1}}
        pass # na podstawie probabila podejmuje decyzje

    def execute_transaction(self, ticker: str, decision: dict, price: float, day: int) -> dict or None:
        if decision['action'] == 'buy':
            if self.curr_asset < price * decision['quantity']:
                raise ValueError(f"Cannot buy {ticker} because asset is not enough")

            self.curr_asset -= price * decision['quantity']
            self.bought[ticker] = {'day': day, 'price': price, 'quantity': decision['quantity']} # co zrobic, gdy dokupujemy te sama, ale dzien pozniej np. w innej cenie
            return {'ticker': ticker, 'action': decision['action'], 'price': price, 'quantity': decision['quantity']}

        if decision['action'] == 'sell':
            if self.bought[ticker]['day'] + self.minimum_holding_period < day:
                raise ValueError(f"Cannot sell {ticker} because it is not held for minimum holding period")

            self.curr_asset += price * self.bought[ticker]['quantity']
            self.profit += self.bought[ticker]['quantity'] * (self.bought[ticker]['price'] - price)
            return {'ticker': ticker, 'action': decision['action'], 'price': price, 'quantity': decision['quantity']}

        return None

    def get_total_profit(self) -> float:
        return self.profit

    def check_loss(self) -> bool:
        if self.profit < -self.max_loss*self.START_ASSET:
            return True
        return False