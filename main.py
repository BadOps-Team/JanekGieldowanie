from Stocks.period import Period
from datetime import date
from Stocks.stock_utility import StockUtility
from Stocks.stock_estimators_builder import *

def main():
    period = Period(date(2019, 1, 1), date(2020, 1, 1)) 
    print(period)
    apple_stock =  StockUtility('AAPL')
    apple_data = apple_stock.get_historical_data(period=period)
    print(apple_data.Close)
    estimator = (EstimatorBuilder.create_builder()
                 .with_startegy(EstimatorStrategy.METHOD_OF_MOMENTS)
                 .with_stock_util(apple_stock)
                 .build())
    results = estimator.estimate_from_historic(period, 10)
    print(results)
    

if __name__ == "__main__":
    main()
