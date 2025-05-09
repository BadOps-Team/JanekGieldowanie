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

                # assign on the very first agent, or any strictly-better profit
                if best_agent is None or agent.profit > best_price:
                    best_price = agent.profit
                    best_agent = agent

                print(f'{agent.profit} {agent.sale_history}')

        # best_agent is now guaranteed not to be None
        print(f'Best price: {best_price:.2f}  History: {best_agent.sale_history}')

    # def summarize_results(self, results):
    #     start_asset = self.agent.START_ASSET
    #     end_asset = self.agent.curr_asset
    #     net_change = end_asset - start_asset
    #     buys = [r for r in results if r['action'] == 'buy']
    #     sells = [r for r in results if r['action'] == 'sell']
    #     print("Simulation Summary:")
    #     print(f"Starting asset value: {start_asset:.2f}")
    #     print(f"Ending asset value:   {end_asset:.2f}")
    #     print(f"Net change:           {net_change:.2f}")
    #     print(f"Total buys executed:  {len(buys)}")
    #     print(f"Total sells executed: {len(sells)}")
    #     print(f"Profit from trades:   {self.agent.get_total_profit():.2f}")

