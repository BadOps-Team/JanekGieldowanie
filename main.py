import json
import sys
from pathlib import Path
from math import inf
from datetime import datetime

from Algorithm import GeneticAlgorithm, Genome
from Simulation import Simulation
from Stocks import StockUtilityFactory, Period
from Stocks.estimators import EstimatorStrategy
from Util import DirectoryUtil

def main(name):
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
    forecast_days = cfg['forecast_days']

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
    for _ in range(size):
        genome = Genome.warm_start(stocks=stocks, historical_prices=historical_prices,
                                   start_asset=start_asset, max_actions_per_day_bought=max_buy,
                                   max_actions_per_day_sold=max_sell, simulation_length=simulation_length, forecast_days=forecast_days)
        agent = genome.to_agent()
        agent.execute(historical_prices=historical_prices, start_asset=start_asset)
        agents.append(agent)

    GA = GeneticAlgorithm(ga_params)
    simulation = Simulation(agents, stocks, start_asset, simulation_length, GA, historical_prices)
    agents_list, days_best_agent, best_agent = simulation.run_simulation(name)
    return [{'profit': a.profit, 'history': a.sale_history} for a in agents_list], [dba - start_asset for dba in days_best_agent], [ba - start_asset for ba in best_agent]

if __name__ == "__main__":
    main_dir = Path(__file__).parent
    DirectoryUtil.directory_exists(main_dir, "graph", True)
    DirectoryUtil.directory_exists(main_dir, "csv_results", True)
    main(sys.argv[1])