from Stocks import StockUtilityFactory
from Stocks.estimators import EstimatorStrategy
from time import time

def main():
    stock_factory = StockUtilityFactory(EstimatorStrategy.METHOD_OF_MOMENTS, 'config.json')
    
    apple_stock = stock_factory.create_stock_utility('AAPL')
    flag = True
    start = time() 
    for estimation in apple_stock.get_estimations():
        #print(estimation)
        if flag:
            print(estimation)
            flag = False
    
    print(f'total time: {time()-start}')

if __name__ == "__main__":
    main()
