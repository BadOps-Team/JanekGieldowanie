import json
import sys
from pathlib import Path
from math import inf
from datetime import datetime
import argparse

from Algorithm import GeneticAlgorithm, Genome
from Simulation import Simulation
from Stocks import StockUtilityFactory, Period
from Stocks.estimators import EstimatorStrategy
from Util import DirectoryUtil

def main(name, it=0):
    with open(name, encoding='utf-8-sig') as f:
        cfg = json.load(f)

    size = cfg['size']
    start_date = datetime.strptime(cfg['start_date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(cfg['end_date'], '%Y-%m-%d').date()
    start_asset = cfg['start_asset']
    tickers = cfg['stocks']
    ga_params = cfg['ga']
    max_buy = cfg['max_actions_per_day']['buy']
    max_sell = cfg['max_actions_per_day']['sell']
    strategy = cfg['estimator_strategy']
    num_of_iterations = cfg['num_of_iterations']

    if strategy == 'mom':
        factory = StockUtilityFactory(EstimatorStrategy.METHOD_OF_MOMENTS, name)
    elif strategy == 'lse':
        factory = StockUtilityFactory(EstimatorStrategy.LEAST_SQUARE_METHOD, name)
    elif strategy == 'ml':
        factory = StockUtilityFactory(EstimatorStrategy.MAXIMUM_LIKELIHOOD, name)
    else:
        raise ValueError('Strategy not recognized')

    stocks = [(t, factory.create_stock_utilty(t)) for t in tickers]

    period = Period(start_date, end_date)
    historical_prices = {}
    simulation_length = inf
    for ticker, stock_utility in stocks:
        historical_prices[ticker] = stock_utility.get_historical_close_prices(period).tolist()
        simulation_length = min(len(historical_prices[ticker]), simulation_length)

    agents = []
    i = 0
    while len(agents) < size:
        genome = Genome.warm_start(stocks=stocks, historical_prices=historical_prices,
                                   start_asset=start_asset, max_actions_per_day_bought=max_buy,
                                   max_actions_per_day_sold=max_sell, simulation_length=simulation_length)
        agent = genome.to_agent()
        agent.execute(historical_prices=historical_prices, start_asset=start_asset)
        if agent.profit > 0:
            agents.append(agent)
            print(f"Agent number {len(agents)} has been added")
        i += 1
        if i >= size * 100:
            raise Exception("Warm start failed, change configuration")

    GA = GeneticAlgorithm(ga_params)
    simulation = Simulation(agents, stocks, start_asset, num_of_iterations, GA, historical_prices, it)
    best_agent, iteration_best_agent, best_agents_profit = simulation.run_simulation(name)
    return {'profit': best_agent.profit, 'history': best_agent.sale_history}, [dba - start_asset for dba in iteration_best_agent], [ba - start_asset for ba in best_agents_profit]

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--config", "-c", help="Path to the configuration file", type=str, default="config/config1_0.json")
    argparser.add_argument("--test", "-t", help="should run estimation tests", action="store_true", default=False)
    argparser.add_argument("--iter", "-i", help="pass iteration number", type=int, default=0)

    args = argparser.parse_args()

    if args.test:
        from tests import EstimatorsTests

        est_test = EstimatorsTests()
        est_test.run_tests()
        exit(0)

    main_dir = Path(__file__).parent
    DirectoryUtil.directory_exists(main_dir, "graphs", True)
    DirectoryUtil.directory_exists(main_dir, "csv_results", True)
    main(args.config)