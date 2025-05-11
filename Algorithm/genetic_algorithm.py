import sys
sys.path.append("..")

from Agent.agent import Agent, PDF

from dataclasses import dataclass
import numpy as np
from typing import Self
import scipy
import random

@dataclass
class Genome:
    minimum_holding_period: int
    probability_distribution: PDF
    max_loss: float
    minimum_bought: int
    stop_loss: float
    take_profit: float

    def from_agent(agent: Agent) -> Self:
        init_dict = vars(agent)
        init_dict = {key: init_dict[key] for key in vars(Genome.random())}
        return Genome(**init_dict)

    def to_agent(self, asset) -> Agent:
        return Agent(asset=asset, **vars(self))

    def random() -> Self:
        xs = np.linspace(0, 1, 1000)
        random_pdf = PDF(scipy.stats.norm.pdf(xs, 0.5, 0.1).tolist())

        return Genome(
            minimum_holding_period = random.randint(0, 10),
            probability_distribution = random_pdf,
            max_loss = np.random.uniform(0, 1),
            minimum_bought = random.randint(0, 10),
            stop_loss = np.random.uniform(0, 1),
            take_profit = np.random.uniform(0, 5)
        )

class GeneticAlgorithm:
    def __init__(
        self, 
        children_ratio: float = 0.3,
        crossover_imbalance: float = 0.25,
        float_mutation_variance: float = 0.1,
        int_mutation_variance: float = 5,
        pdf_mutation_variance: float = 0.1,
        chromosome_mutation_chance: float = 0.05
    ):
        self.children_ratio = children_ratio
        self.crossover_imbalance = crossover_imbalance
        self.float_mutation_variance = float_mutation_variance
        self.int_mutation_variance = int_mutation_variance
        self.pdf_mutation_variance = pdf_mutation_variance
        self.chromosome_mutation_chance = chromosome_mutation_chance

    def crossover_float(self, float1: float, float2: float) -> float:
        beta = np.random.uniform(-self.crossover_imbalance, 1+self.crossover_imbalance)
        return float1*beta + float2*(1-beta)

    def crossover_int(self, int1: int, int2: int) -> int:
        return round(self.crossover_float(int1, int2))

    def crossover_pdf(self, pdf1: PDF, pdf2: PDF) -> PDF:
        crossed_points = [self.crossover_float(float1, float2) for float1, float2 in zip(pdf1.function, pdf2.function)]
        return PDF(crossed_points)

    def crossover(self, parent1: Genome, parent2: Genome) -> Genome:
        return Genome(
            minimum_holding_period = self.crossover_int(parent1.minimum_holding_period, parent2.minimum_holding_period),
            probability_distribution = self.crossover_pdf(parent1.probability_distribution, parent2.probability_distribution),
            max_loss = self.crossover_float(parent1.max_loss, parent2.max_loss),
            minimum_bought = self.crossover_int(parent1.minimum_bought, parent2.minimum_bought),
            stop_loss = self.crossover_float(parent1.stop_loss, parent2.stop_loss),
            take_profit = self.crossover_float(parent1.take_profit, parent2.take_profit)
        )

    def mutate_float(self, value: float) -> float:
        if np.random.random() < self.chromosome_mutation_chance:
            return value + np.random.normal(0, self.float_mutation_variance)
        else:
            return value

    def mutate_int(self, value: int) -> int:
        if np.random.random() < self.chromosome_mutation_chance:
            return value + round(np.random.normal(0, self.int_mutation_variance))
        else:
            return value

    def mutate_pdf(self, value: PDF) -> PDF:
        if np.random.random() < self.chromosome_mutation_chance:
            xs = np.linspace(0, 1, 1000)
            mutate_pdf = PDF(scipy.stats.norm.pdf(xs, 0.5, 0.1))
            return self.crossover_pdf(value, mutate_pdf)
        else:
            return value
    
    def mutate(self, agent: Genome) -> Genome:
        return Genome(
            minimum_holding_period = self.mutate_int(agent.minimum_holding_period),
            probability_distribution = self.mutate_pdf(agent.probability_distribution),
            max_loss = self.mutate_float(agent.max_loss),
            minimum_bought = self.mutate_int(agent.minimum_bought),
            stop_loss = self.mutate_float(agent.stop_loss),
            take_profit = self.mutate_float(agent.take_profit)
        )

    def evolve(self, start_asset, agents: list[Agent]) -> list[Agent]:
        fitness = [agent.get_total_profit() for agent in agents]
        fitness = [el/sum(fitness) for el in fitness]

        children = []
        children_size = int(len(agents)*self.children_ratio)
        while len(children) < children_size: 
            parent1 = np.random.choice(agents, p=fitness)
            parent2 = np.random.choice(agents, p=fitness)

            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            children.append(child.to_agent(start_asset))
        
        alive_size = len(agents)-len(children)
        alive = np.random.choice(
            agents, 
            size=alive_size,
            replace=False,
            p=fitness
        ).tolist()

        return alive + children

# Tak to powinno działać
if __name__ == '__main__':
    size = 100
    agents = []
    for _ in range(size):
        agent = Agent(asset='abc', **vars(Genome.random()))
        agent.profit = random.randint(0, 10)
        agents.append(agent)

    GA = GeneticAlgorithm()

    for agent in agents:
        print(f'{agent.profit}, {agent.max_loss}, {agent.stop_loss}')

    agents = GA.evolve('abc', agents)
    
    print()
    for agent in agents:
        print(f'{agent.profit}, {agent.max_loss}, {agent.stop_loss}, {agent.probability_distribution()}')
