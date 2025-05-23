import random
from Agent import Agent
import numpy as np
from .algorithm_settings import GASettings
from .genome import Genome

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

        self.agent_life_lengths = []

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

        fitness = [f / sum_fitness for f in fitness]

        children = []
        children_size = int(len(agents) * self.settings.children_ratio)
        while len(children) < children_size:
            parent1 = Genome.from_agent(np.random.choice(agents, p=fitness))
            parent2 = Genome.from_agent(np.random.choice(agents, p=fitness))
            child = parent1.crossover(parent2, self.settings)
            child.mutate(self.settings)
            child_agent = child.to_agent()
            child_agent.age = 0
            children.append(child_agent)

        alive_size = len(agents) - len(children)
        alive_indices = np.random.choice(range(len(agents)), size=alive_size, p=fitness).tolist()
        
        alive = np.array(agents)[alive_indices]
        for agent in alive:
            agent.age += 1

        dead = np.delete(agents, alive_indices)
        for agent in dead:
            self.agent_life_lengths.append(agent.age)

        return alive.tolist() + children
