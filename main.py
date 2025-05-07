import random
from Algorithm.genetic_algorithm import GeneticAlgorithm, Genome
from Simulation.simulation import Simulation
from Stocks import StockUtilityFactory
from Stocks.estimators import EstimatorStrategy

# config:
# size - ile agentów
# dni - na ich podstawie masz obliczyc estymator
# dni jako dni ewolucji
# to co jest aktualnie w configu
# (wybieranie krzyżowania ????????)
# kapitał początkowy
# jakie firmy lub liczba

def main():
    factory = StockUtilityFactory(EstimatorStrategy.METHOD_OF_MOMENTS, 'config.json')
    apple_stock = factory.create_stock_utilty('AAPL')
    spotify_stock = factory.create_stock_utilty('SPOT')
    stocks = [apple_stock, spotify_stock]
    start_asset = 1000
    evolution_days = 10

    size = 100
    agents = []
    for _ in range(size):
        agent = Genome.random().to_agent()
        agent.profit = random.randint(0, 10) # asset
        agents.append(agent)

    GA = GeneticAlgorithm()
    simulation = Simulation(agents, stocks, start_asset, evolution_days, GA)
    simulation.run_simulation()

    # for agent in agents:
    #     print(f'{agent.profit} {agent.sale_history}')
    #
    # agents = GA.evolve(agents)
    #
    # print()
    # for agent in agents:
    #     print(f'{agent.profit} {agent.sale_history}')

if __name__ == "__main__":
    main()