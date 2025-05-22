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
        iteration_best_agents_profit = []
        for i in range(self.num_of_iterations):
            print("=" * 100)
            self.agents = self.GA.evolve(self.agents)
            iteration_best_agent = None
            for agent in self.agents:
                agent.execute(historical_prices=self.historical_prices, start_asset=self.start_asset)

                if best_agent is None or agent.profit > best_profit:
                    best_profit = agent.profit
                    best_profit_idx = i
                    best_agent = agent
                if iteration_best_agent is None or agent.profit > iteration_best_agent.profit:
                    iteration_best_agent = agent

            iteration_best_agents_profit.append(iteration_best_agent.profit)
            best_agents_profit.append(best_agent.profit)

            self.GA.agent_life_lengths += [agent.age for agent in self.agents]
            print(f"Iteration {i} best agent: Agent{self.agents.index(iteration_best_agent)}, profit = {iteration_best_agent.profit - self.start_asset}")
            print(f"Best profit so far = {best_agent.profit - self.start_asset}, found in iteration = {best_profit_idx}")

        print(f"Best agent sale history: {best_agent.sale_history}")
        self.export_to_csv(
            filename=filename, 
            best_agents_profit=best_agents_profit,
            iteration_best_agents_profit=iteration_best_agents_profit,
            median_agent_age=statistics.median(self.GA.agent_life_lengths),
            mean_agent_age=statistics.mean(self.GA.agent_life_lengths),
            best_agent=best_agent
        )
        return best_agent, iteration_best_agents_profit, best_agents_profit

    def export_to_csv(self, filename, best_agents_profit, iteration_best_agents_profit, median_agent_age, mean_agent_age, best_agent):
        results_df = pd.DataFrame({
            "iteration": list(range(self.num_of_iterations)),
            "best_agent_profit": best_agents_profit,
            "iteration_best_agent_profit": iteration_best_agents_profit
        })

        stats_df = pd.DataFrame({
            "median_agent_age": [median_agent_age],
            "mean_agent_age": [mean_agent_age],
            "best_sale_history": [str(best_agent.sale_history)]
        })

        file_path = Path(filename).name
        results_path = Path(__file__).parent.parent / "csv_results"
        results_path.mkdir(parents=True, exist_ok=True)
        results_df.to_csv(results_path / (
                    f"results_it{self.it}_" + file_path.replace(".json", ".csv")))
        stats_df.to_csv(results_path / (f"results_stats{self.it}_" + file_path.replace(".json", ".csv")))