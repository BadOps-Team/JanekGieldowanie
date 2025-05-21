import sys

from Stocks import StockUtility

sys.path.append("..")
import sys

from Stocks import StockUtility

sys.path.append("..")

from Agent.agent import Agent

from dataclasses import dataclass
import numpy as np
from typing import Self
import random

@dataclass
class GASettings:
    children_ratio: float = 0.3
    crossover_imbalance: float = 0.25
    float_mutation_variance: float = 0.1
    rotation_size_variance: float = 1
    rotation_shift_variance: float = 1
    mutate_change_chance: float = 0.5
    mutate_rotate_chance: float = 0.5
    crossover_point_amount: int = 2
    crossover_point_chance: float = 0.5

@dataclass
class Gene:
    content: list[float]

    @staticmethod
    def mutate_float(value: float, settings) -> float:
        return value + float(np.random.normal(0, settings.float_mutation_variance))

    def mutate_change(self, settings):
        i = random.randrange(len(self.content))
        self.content[i] = self.mutate_float(self.content[i], settings)

    def mutate_rotate(self, settings):
        new_content = self.content.copy()
        start = random.randrange(len(self.content))
        size = int(np.random.lognormal(0, settings.rotation_size_variance))
        shift = int(np.random.lognormal(0, settings.rotation_shift_variance))
        if size == 1:
            return

        for i in range(size):
            cur_pos = (start+i) % len(self.content)
            target_pos = (cur_pos+shift) % len(self.content)
            if i >= size-shift:
                target_pos = (target_pos+len(self.content)-size) % len(self.content)

            new_content[cur_pos] = self.content[target_pos]
        
        self.content = new_content

    def mutate(self, settings):
        if np.random.random() < settings.mutate_change_chance:
            self.mutate_change(settings)
        if np.random.random() < settings.mutate_rotate_chance:
            self.mutate_rotate(settings)

    def crossover_point(self, other: Self, settings) -> Self:
        child1 = self.content
        child2 = other.content
        for _ in range(settings.crossover_point_amount):
            point = random.randrange(len(self.content))

            left1 = child1[:point]
            right1 = child1[point:]
            left2 = child2[:point]
            right2 = child2[point:]

            child1 = left1 + right2
            child2 = left2 + right1

        return Gene(child1) if random.random() < 0.5 else Gene(child2)

    @staticmethod
    def crossover_float(float1: float, float2: float, settings) -> float:
        beta = np.random.uniform(-settings.crossover_imbalance, 1+settings.crossover_imbalance)
        return float1*beta + float2*(1-beta)

    def crossover_uniform(self, other: Self, settings) -> Self:
        new_gene = Gene([0 for _ in range(len(self.content))])
        for i in range(len(self.content)):
            new_gene.content[i] = self.crossover_float(self.content[i], other.content[i], settings)
        
        return new_gene
    
    def crossover(self, other: Self, settings) -> Self:
        if random.random() < settings.crossover_point_chance:
            return self.crossover_point(other, settings)
        else:
            return self.crossover_uniform(other, settings)

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
                   forecast_days: int, start_asset: float, max_actions_per_day_bought: int, max_actions_per_day_sold: int) -> Self:
        sale_history = {ticker: [] for ticker, _ in stocks}
        curr_asset = start_asset
        inventory = {ticker: 0 for ticker, _ in stocks}

        predictions = {
            ticker: next(stock_utility.get_estimations()).estimated_prices[:forecast_days]
            for ticker, stock_utility in stocks
        }

        last_known_prices = {
            ticker: historical_prices[ticker][-1]
            for ticker, _ in stocks
        }

        for day in range(forecast_days):
            tickers_shuffled = stocks[:]
            random.shuffle(tickers_shuffled)  # tutaj losujemy kolejność tickerów na każdy dzień

            for ticker, _ in tickers_shuffled:
                prev_price = last_known_prices[ticker] if day == 0 else predictions[ticker][day - 1]
                future_price = predictions[ticker][day]

                price_change_ratio = (future_price - prev_price) / prev_price
                action = 0

                if price_change_ratio > 0.001:
                    max_affordable = int(curr_asset / prev_price)
                    if max_affordable > 0:
                        # TODO estimate amount of actions
                        action = random.randint(1, min(max_affordable, max_actions_per_day_bought))
                        curr_asset -= action * prev_price
                        inventory[ticker] += action

                elif price_change_ratio < -0.0001 and inventory[ticker] > 0:
                    # TODO estimate amount of actions
                    action = -random.randint(1, min(inventory[ticker], max_actions_per_day_sold))
                    curr_asset -= action * prev_price
                    inventory[ticker] += action

                sale_history[ticker].append(action)

        sale_history = {ticker: Gene(actions) for ticker, actions in sale_history.items()}

        return cls(sale_history=sale_history)

    

class GeneticAlgorithm:
    def __init__(self, ga_config=None):
        self.settings = GASettings()
        if ga_config:
            self.settings.children_ratio = ga_config["children_ratio"]
            self.settings.crossover_imbalance = ga_config["crossover_imbalance"]
            self.settings.float_mutation_variance = ga_config["float_mutation_variance"]
            self.settings.rotation_size_variance = ga_config["rotation_size_variance"]
            self.settings.rotation_shift_variance = ga_config["rotation_shift_variance"]
            self.settings.mutate_change_chance = ga_config["mutate_change_chance"]
            self.settings.mutate_rotate_chance = ga_config["mutate_rotate_chance"]
            self.settings.crossover_point_amount = ga_config["crossover_point_amount"]
            self.settings.crossover_point_chance = ga_config["crossover_point_chance"]


    def evolve(self, agents: list[Agent]) -> list[Agent]:
        fitness = [agent.profit for agent in agents]
        sum_fitness = sum(fitness)
        if sum_fitness == 0:
            agents_next = []
            for agent in agents:
                child = Genome.from_agent(agent)
                child.mutate(self.settings)
                agents_next.append(child.to_agent())
            return agents_next

        # Normalizacja fitness
        fitness = [f / sum_fitness for f in fitness]

        # Generowanie dzieci
        children = []
        children_size = int(len(agents) * self.settings.children_ratio)
        while len(children) < children_size:
            parent1 = Genome.from_agent(np.random.choice(agents, p=fitness))
            parent2 = Genome.from_agent(np.random.choice(agents, p=fitness))
            child = parent1.crossover(parent2, self.settings)
            child.mutate(self.settings)
            children.append(child.to_agent())

        # Selekcja przetrwałych
        alive_size = len(agents) - len(children)
        alive = np.random.choice(agents, size=alive_size, p=fitness).tolist()

        return alive + children
