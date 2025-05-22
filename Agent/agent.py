from typing import List, Dict

class Agent:
    def __init__(self, sale_history: Dict[str, List[int]]):
        # Taki słownik: {
        #   'ticker1': [1, 2, -1, -2, 3] <- Tyle elementów listy ile dni, dodatni to kupno, ujemny to sprzedaż
        #   'ticker2': [9, 2, -2, 3, 0] 
        # }
        self.sale_history = sale_history
        self.profit = 0
        self.age = 0

    def execute(self, historical_prices, start_asset):
        curr_asset = start_asset
        inventory = {ticker: 0 for ticker in self.sale_history}

        for i in range(len(next(iter(self.sale_history.values())))):
            for ticker, actions in self.sale_history.items():
                action = actions[i]
                inventory[ticker] += action
                if inventory[ticker] < 0:
                    self.profit = 0
                    return

                curr_asset -= historical_prices[ticker][i] * action
            if curr_asset < 0:
                self.profit = 0
                return


        for ticker, count in inventory.items():
            curr_asset += historical_prices[ticker][-1] * count

        self.profit = curr_asset
