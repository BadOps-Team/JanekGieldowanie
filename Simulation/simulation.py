from typing import List, Dict
from Agent import Agent
from Algorithm import GeneticAlgorithm
from Stocks import StockUtility
import pandas as pd
from pathlib import Path
import statistics

class Simulation:
    def __init__(self, agents: List[Agent], stock_utilities: List[tuple[str, StockUtility]],
                 start_asset: int, num_of_iterations: int, GA: GeneticAlgorithm,
                 historical_prices: Dict[str, List[int]], it: int):
        self.agents = agents
        self.stock_utilities = stock_utilities
        self.start_asset = start_asset
        self.num_of_iterations = num_of_iterations
        self.GA = GA
        self.historical_prices = historical_prices
        self.it = it

    def run_simulation(self, filename):
        best_agent = None
        best_profit = 0
        best_profit_idx = None
        best_agents_profit = []
        day_best_agents_profit = []
        for i in range(self.num_of_iterations):
            print("=" * 100)
            self.agents = self.GA.evolve(self.agents)
            day_best_agent = None
            for agent in self.agents:
                agent.execute(historical_prices=self.historical_prices, start_asset=self.start_asset)

                if best_agent is None or agent.profit > best_profit:
                    best_profit = agent.profit
                    best_profit_idx = i
                    best_agent = agent
                if day_best_agent is None or agent.profit > day_best_agent.profit:
                    day_best_agent = agent    

            day_best_agents_profit.append(day_best_agent.profit)
            best_agents_profit.append(best_agent.profit)
            print(f"Iteration {i} best agent: Agent{self.agents.index(day_best_agent)}, profit = {day_best_agent.profit - self.start_asset}")
            print(f"Best profit so far = {best_agent.profit - self.start_asset}, found in iteration = {best_profit_idx}")

        print(f"Best agent sale history: {best_agent.sale_history}")
        self.export_to_csv(
            filename=filename, 
            best_agents_profit=best_agents_profit, 
            day_best_agents_profit=day_best_agents_profit, 
            median_agent_age=statistics.median(self.GA.agent_life_lengths),
            mean_agent_age=statistics.mean(self.GA.agent_life_lengths)
        )
        return self.agents, day_best_agents_profit, best_agents_profit

    def export_to_csv(self, filename, best_agents_profit, day_best_agents_profit, median_agent_age, mean_agent_age):
        results_agents_df = pd.DataFrame([{
            "profit": agent.profit,
            "age": agent.age,
            "sale_history": agent.sale_history
        } for agent in self.agents])

        results_df = pd.DataFrame({
            "day": list(range(self.num_of_iterations)),
            "best_agent_profit": best_agents_profit,
            "day_best_agent_profit": day_best_agents_profit
        })

        stats_df = pd.DataFrame({
            "median_agent_age": [median_agent_age],
            "mean_agent_age": [mean_agent_age]
        })

        file_path = Path(filename).name
        results_path = Path(__file__).parent.parent / "csv_results"
        results_path.mkdir(parents=True, exist_ok=True)
        results_df.to_csv(results_path / (
                    f"results_it{self.it}_" + file_path.replace(".json", ".csv")))
        results_agents_df.to_csv(results_path / (f"results_agents_it{self.it}_" + file_path.replace(".json", ".csv")))
        stats_df.to_csv(results_path / (f"results_stats{self.it}_" + file_path.replace(".json", ".csv")))