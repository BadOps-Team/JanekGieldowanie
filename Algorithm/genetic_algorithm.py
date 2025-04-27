import random

from Agent.agent import Agent
from Simulation.simulation import Simulation


class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = [self.random_strategy() for _ in range(population_size)]

    def random_strategy(self):
        return {
            'stop_loss': random.uniform(0.7, 0.95),
            'take_profit': random.uniform(1.00, 1.10)  # allow 1.00–1.10
        }

    def evaluate_fitness(self, agent, stock_utility):
        # Clone agent to reset state for each strategy evaluation
        agent_copy = Agent(
            asset=agent.START_ASSET,
            minimum_holding_period=agent.minimum_holding_period,
            strategy=agent.strategy,
            max_loss=agent.max_loss,
            probability_distribution=agent.probability_distribution
        )
        # Apply strategy thresholds
        agent_copy.stop_loss = agent.stop_loss
        agent_copy.take_profit = agent.take_profit

        # Run simulation on the cloned agent
        simulation = Simulation(agent_copy, stock_utility)
        simulation.run_simulation()
        return agent_copy.get_total_profit()

    def run_generation(self, agent, stock_utility):
        fitness_scores = []
        for strategy in self.population:
            agent.stop_loss = strategy['stop_loss']
            agent.take_profit = strategy['take_profit']
            fitness = self.evaluate_fitness(agent, stock_utility)
            fitness_scores.append((fitness, strategy))

        # sort by fitness (float) only
        fitness_scores.sort(key=lambda x: x[0], reverse=True)

        # keep top half
        survivors = [strategy for _, strategy in fitness_scores[: self.population_size // 2]]
        self.population = survivors.copy()

        # reproduce to fill population
        while len(self.population) < self.population_size:
            parent = random.choice(survivors)
            child = parent.copy()
            if random.random() < self.mutation_rate:
                child['stop_loss'] = max(0.0, min(1.0, child['stop_loss'] + random.uniform(-0.05, 0.05)))
                child['take_profit'] = max(1.0, child['take_profit'] + random.uniform(-0.05, 0.05))
            self.population.append(child)

