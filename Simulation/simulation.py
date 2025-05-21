from typing import List, Dict
from Agent.agent import Agent
from Algorithm.genetic_algorithm import GeneticAlgorithm
from Stocks import StockUtility

class Simulation:
    def __init__(self, agents: List[Agent], stock_utilities: List[tuple[str, StockUtility]],
                 start_asset: int, evolution_days: int, GA: GeneticAlgorithm,
                 historical_prices: Dict[str, List[int]]):
        self.agents = agents
        self.stock_utilities = stock_utilities
        self.start_asset = start_asset
        self.evolution_days = evolution_days
        self.GA = GA
        self.historical_prices = historical_prices

    def run_simulation(self):
        best_agent = None
        best_price = 0

        for i in range(self.evolution_days):
            self.agents = self.GA.evolve(self.agents)
            for agent in self.agents:
                agent.execute(historical_prices=self.historical_prices, start_asset=self.start_asset)

                if best_agent is None or agent.profit > best_price:
                    best_price = agent.profit
                    best_agent = agent

                print(f'{agent.profit} {agent.sale_history}')

        print(f'Best price: {best_price:.2f}  History: {best_agent.sale_history}')
        return self.agents

