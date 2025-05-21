from typing import List, Dict
from Agent import Agent
from Algorithm import GeneticAlgorithm
from Stocks import StockUtility
import pandas as pd
from pathlib import Path

class Simulation:
    def __init__(self, agents: List[Agent], stock_utilities: List[tuple[str, StockUtility]],
                 start_asset: int, simulation_length: int, GA: GeneticAlgorithm,
                 historical_prices: Dict[str, List[int]]):
        self.agents = agents
        self.stock_utilities = stock_utilities
        self.start_asset = start_asset
        self.simulation_length = simulation_length
        self.GA = GA
        self.historical_prices = historical_prices

    def run_simulation(self, filename):
        best_agent = None
        best_profit = 0
        best_agents_profit = []
        day_best_agents_profit = []
        for i in range(self.simulation_length):
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

        results_agents_df = pd.DataFrame([{
            "profit": agent.profit,
            "age": agent.age,
            "sale_history": agent.sale_history
        } for agent in self.agents])

        results_df = pd.DataFrame({
            "day": list(range(self.simulation_length)),
            "best_agent_profit": best_agents_profit,
            "day_best_agent_profit": day_best_agents_profit
        })

        file_path = Path(filename).name
        results_path = Path(__file__).parent.parent / "csv_results"
        results_df.to_csv(results_path / ("results_" + file_path.replace(".json", ".csv")))
        results_agents_df.to_csv(results_path / ("results_agents_" + file_path.replace(".json", ".csv")))
        
        return self.agents, day_best_agents_profit, best_agents_profit

