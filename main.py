from Stocks.period import Period
from datetime import date
from Stocks.stock_utility import StockUtility

def main():
    period = Period(date(2010, 1, 1), date(2020, 1, 1)) 
    print(period)
    apple_stock =  StockUtility('AAPL')
    apple_data = apple_stock.get_historical_data(period=period)
    print(apple_data)
    apple_stock.save_data()

if __name__ == "__main__":
    main()
