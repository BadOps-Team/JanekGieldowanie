from typing import List, Dict
from Agent import Agent
from Algorithm import GeneticAlgorithm
from Stocks import StockUtility
import pandas as pd
from pathlib import Path

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
        best_profit = 0
        best_agents_profit = []
        day_best_agents_profit = []
        for i in range(self.evolution_days):
            print("=" * 100)
            print(f"Day {i}")
            self.agents = self.GA.evolve(self.agents)
            day_best_agent = None
            for agent in self.agents:
                agent.execute(historical_prices=self.historical_prices, start_asset=self.start_asset)

                if best_agent is None or agent.profit > best_profit:
                    best_profit = agent.profit
                    best_agent = agent
                if day_best_agent is None or agent.profit > day_best_agent.profit:
                    day_best_agent = agent    

            day_best_agents_profit.append(day_best_agent.profit)
            best_agents_profit.append(best_agent.profit)
            print(f"Days {i} best agent: Agent{self.agents.index(day_best_agent)} profit = {day_best_agent.profit - self.start_asset}")
            print(f"Best profit so far = {best_agent.profit - self.start_asset}")

        result_df = pd.DataFrame(self.agents)
        result_df["day_best_agents_profit"] = day_best_agents_profit
        result_df["best_agents_profit"] = best_agents_profit

        results_path = Path(__file__).parent / "csv_results"
        result_df.to_csv(results_path / "simulation.csv")
        return self.agents, day_best_agents_profit, best_agents_profit

