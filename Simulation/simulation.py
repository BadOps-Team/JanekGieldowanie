import datetime

from Agent.agent import Agent
from Stocks import StockUtility


class Simulation:
    def __init__(self, agent: Agent, stock_utility: StockUtility):
        self.agent = agent
        self.stock_utility = stock_utility

    def run_simulation(self):
        estimations = list(self.stock_utility.get_estimations())
        start_date = StockUtility._ESTIMATION_CONFIG.start_date
        length = StockUtility._ESTIMATION_CONFIG.simulation_length
        results = []

        for day_offset in range(length):
            current_prices = {}
            # Build price map
            for est in estimations:
                ticker = self.stock_utility.stock_name
                idx = min(day_offset, len(est.estimated_prices) - 1)
                current_prices[ticker] = est.estimated_prices[idx]

            # Decisions
            decisions = self.agent.make_decision(
                current_prices,
                {t: est.estimated_prices for t, est in [(self.stock_utility.stock_name, est) for est in estimations]},
                day_offset
            )

            # Execute
            for ticker, decision in decisions.items():
                tx = self.agent.execute_transaction(
                    ticker=ticker,
                    decision=decision,
                    price=current_prices[ticker],
                    day=day_offset
                )
                results.append(tx)

            if self.agent.check_loss():
                break

                # Hard stop: liquidate remaining positions at last known price
        if estimations:
            # determine last price map
            last_price = estimations[-1].estimated_prices[-1]
            for ticker, txns in list(self.agent.bought.items()):
                # iterate over a copy so popping doesn't skip entries
                for txn in txns.copy():
                    decision = {'action': 'sell', 'quantity': txn['quantity']}
                    tx = self.agent.execute_transaction(
                        ticker=ticker,
                        decision=decision,
                        price=last_price,
                        day=length - 1
                    )
                    results.append(tx)
            # no need to manually clear; execute_transaction removes each txn

        self.summarize_results(results)
        return results

    def summarize_results(self, results):
        start_asset = self.agent.START_ASSET
        end_asset = self.agent.curr_asset
        net_change = end_asset - start_asset
        buys = [r for r in results if r['action'] == 'buy']
        sells = [r for r in results if r['action'] == 'sell']
        print("Simulation Summary:")
        print(f"Starting asset value: {start_asset:.2f}")
        print(f"Ending asset value:   {end_asset:.2f}")
        print(f"Net change:           {net_change:.2f}")
        print(f"Total buys executed:  {len(buys)}")
        print(f"Total sells executed: {len(sells)}")
        print(f"Profit from trades:   {self.agent.get_total_profit():.2f}")

