from time import time

from Agent.agent import Agent
from Algorithm.genetic_algorithm import GeneticAlgorithm
from Simulation.simulation import Simulation
from Stocks import StockUtilityFactory
from Stocks.estimators import EstimatorStrategy


def main():
    factory = StockUtilityFactory(EstimatorStrategy.METHOD_OF_MOMENTS, 'config.json')
    apple_stock = factory.create_stock_utilty('AAPL')

    agent = Agent(
        asset=1000,
        minimum_holding_period=1,
        probability_distribution=lambda: 0
    )

    ga = GeneticAlgorithm(population_size=10, mutation_rate=0.1)
    print(ga.population)

    print("=== Genetic Algorithm Run ===")
    start = time()
    ga.run_generation(agent, apple_stock)
    print(f"Total GA run time: {time() - start:.2f} seconds")


if __name__ == "__main__":
    main()
