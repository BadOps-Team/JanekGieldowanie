import json
import random
from datetime import datetime

from Agent.agent import Agent
from Algorithm.genetic_algorithm import GeneticAlgorithm, Genome
from Simulation.simulation import Simulation
from Stocks import StockUtilityFactory, Period
from Stocks.estimators import EstimatorStrategy

# config:
# size - ile agentów
# start date
# end date - chodzi o ceny historyczne
# dni jako dni ewolucji
# to co jest aktualnie w configu
# (wybieranie krzyżowania ????????)
# kapitał początkowy
# jakie firmy lub liczba
# parametry z algorytmu genetycznego jeszcze


# musisz sie pobawic settingsami do stockow, bo teraz mam ustawione na sztywno zeby generowalo 100 dni,
# ale jak lekko pozmieniam parametry to wszedzie sa errory albo pusta tablica xd

def warm_start(stock_utilities, historical_prices, start_asset):
    prices = {}
    for ticker, stock_utility in stock_utilities:
        prices[ticker] = list(stock_utility.get_estimations())[0].estimated_prices

    #jakas logika kupowania

    bought = {}
    print(prices)
    agent = Agent(bought)
    agent.execute(historical_prices=historical_prices, start_asset=start_asset)

def main():

    with open('config.json') as f:
        cfg = json.load(f)

    size = cfg['size']
    start_date = datetime.strptime(cfg['start_date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(cfg['end_date'], '%Y-%m-%d').date()
    evolution_days = cfg['evolution_days']
    forecast_days = cfg['forecast_days']
    estimation_period = cfg['estimation_period']
    simulation_length = cfg['simulation_length']
    start_asset = cfg['start_asset']
    tickers = cfg['stocks']
    ga_params = cfg['ga']
    max_buy = cfg['max_actions_per_day']['buy']
    max_sell = cfg['max_actions_per_day']['sell']

    factory = StockUtilityFactory(EstimatorStrategy.METHOD_OF_MOMENTS, 'config.json')

    stocks = [(t, factory.create_stock_utilty(t)) for t in tickers]

    period = Period(start_date, end_date)
    historical_prices = {}
    for ticker, stock_utility in stocks:
        historical_prices[ticker] = stock_utility.get_historical_close_prices(period).tolist()

    agents = []

    for _ in range(size):
        # warm_start(stocks, historical_prices, start_asset)
        # zostawic ten random tez do testow !!!!!!
        # genome = Genome.random()
        genome = Genome.warm_start(stocks, historical_prices, forecast_days, start_asset, max_buy, max_sell)
        agent = genome.to_agent()
        agent.execute(historical_prices=historical_prices, start_asset=start_asset)
        agents.append(agent)

    GA = GeneticAlgorithm()
    simulation = Simulation(agents, stocks, start_asset, evolution_days, GA, historical_prices)
    simulation.run_simulation()

if __name__ == "__main__":
    main()