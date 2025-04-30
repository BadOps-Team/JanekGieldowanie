import sys
sys.path.append("..")

from Agent.agent import Agent

from dataclasses import dataclass
import numpy as np
from typing import Self
import scipy
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

    def mutate_float(self, value: float, settings) -> float:
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
        our = self.content.copy()
        other = other.content.copy()
        for _ in range(settings.crossover_point_amount):
            point = random.randrange(1, len(self.content))
            tmp = our.copy()
            our = our[:point] + other[point:]
            other = other[:point] + tmp[point:]

        return Gene(our) if random.random() < 0.5 else Gene(other)
    
    def crossover_float(self, float1: float, float2: float, settings) -> float:
        beta = np.random.uniform(-settings.crossover_imbalance, 1+settings.crossover_imbalance)
        return float1*beta + float2*(1-beta)

    def crossover_uniform(self, other: Self, settings) -> Self:
        new_gene = Gene([None for _ in range(len(self.content))])
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

    def from_agent(agent: Agent) -> Self:
        return Genome(
            sale_history = agent.sale_history,
        )

    def to_agent(self) -> Agent:
        return Agent(sale_history=self.sale_history)

    def random() -> Self:
        return Genome(
            sale_history = {
                'abc': Gene([np.random.uniform(-5, 5) for _ in range(5)]),
                'cde': Gene([np.random.uniform(-5, 5) for _ in range(5)])
            }
        )

class GeneticAlgorithm:
    def __init__(self, settings=GASettings()):
        self.settings = settings

    def evolve(self, agents: list[Agent]) -> list[Agent]:
        fitness = [agent.profit for agent in agents]
        fitness = [el/sum(fitness) for el in fitness]

        children = []
        children_size = int(len(agents)*self.settings.children_ratio)
        while len(children) < children_size: 
            parent1 = Genome.from_agent(np.random.choice(agents, p=fitness))
            parent2 = Genome.from_agent(np.random.choice(agents, p=fitness))

            child = parent1.crossover(parent2, self.settings)
            child.mutate(self.settings)
            children.append(child.to_agent())
        
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
        agent = Genome.random().to_agent()
        agent.profit = random.randint(0, 10)
        agents.append(agent)

    GA = GeneticAlgorithm()

    for agent in agents:
        print(f'{agent.profit} {agent.sale_history}')

    agents = GA.evolve(agents)
    
    print()
    for agent in agents:
        print(f'{agent.profit} {agent.sale_history}')
