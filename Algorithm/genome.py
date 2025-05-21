from .gene import Gene
from typing import Self
from dataclasses import dataclass
from Agent import Agent
import numpy as np
from Stocks import StockUtility
import random

@dataclass
class Genome:
    sale_history: dict[str, Gene]

    def mutate(self, settings):
        [gene.mutate(settings) for gene in self.sale_history.values()]

    def crossover(self, other: Self, settings) -> Self:
        new_genome = Genome({})

        for ticker in self.sale_history.keys():
            new_genome.sale_history[ticker] = self.sale_history[ticker].crossover(
                other.sale_history[ticker],
                settings
            )

        return new_genome

    @classmethod
    def from_agent(cls, agent: Agent) -> Self:
        return cls(
            sale_history={
                ticker: Gene(content=history if isinstance(history, list) else history.content)
                for ticker, history in agent.sale_history.items()
            }
        )

    def to_agent(self) -> Agent:
        return Agent(
            sale_history={
                ticker: [int(round(value)) for value in gene.content]
                for ticker, gene in self.sale_history.items()
            }
        )

    @classmethod
    def random(cls) -> Self:
        return cls(
            sale_history = {
                'AAPL': Gene([np.random.uniform(-10, 10) for _ in range(10)]),
                'SPOT': Gene([np.random.uniform(-10, 10) for _ in range(10)])
            }
        )

    @classmethod
    def warm_start(cls, stocks: list[tuple[str, StockUtility]], historical_prices: dict[str, list[float]],
                   start_asset: float, max_actions_per_day_bought: int, max_actions_per_day_sold: int,
                   simulation_length: int) -> Self:
        sale_history = {ticker: [] for ticker, _ in stocks}
        curr_asset = start_asset
        inventory = {ticker: 0 for ticker, _ in stocks}

        predictions = {
            ticker: next(stock_utility.get_estimations()).estimated_prices
            for ticker, stock_utility in stocks
        }

        last_known_prices = {
            ticker: historical_prices[ticker][-1]
            for ticker, _ in stocks
        }

        for day in range(simulation_length):
            tickers_shuffled = stocks[:]
            random.shuffle(tickers_shuffled)

            for ticker, _ in tickers_shuffled:
                prev_price = last_known_prices[ticker] if day == 0 else predictions[ticker][day - 1]
                future_price = predictions[ticker][day]

                price_change_ratio = (future_price - prev_price) / prev_price
                action = 0

                if price_change_ratio > 0.001:
                    max_affordable = int(curr_asset / prev_price)
                    if max_affordable > 0:
                        action = random.randint(1, min(max_affordable, max_actions_per_day_bought))
                        curr_asset -= action * prev_price
                        inventory[ticker] += action

                elif price_change_ratio < -0.0001 and inventory[ticker] > 0:
                    action = -random.randint(1, min(inventory[ticker], max_actions_per_day_sold))
                    curr_asset -= action * prev_price
                    inventory[ticker] += action

                sale_history[ticker].append(action)

            predictions = {
                ticker: next(stock_utility.get_estimations()).estimated_prices
                for ticker, stock_utility in stocks
            }

        sale_history = {ticker: Gene(actions) for ticker, actions in sale_history.items()}

        return cls(sale_history=sale_history)
