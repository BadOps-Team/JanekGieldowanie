from Stocks.period import Period
from Stocks.date_formatter import DateFormatter
from Util.directory_util import DirectoryUtil
from pathlib import Path
import pandas as pd
import yfinance as yf


class StockUtility:
    _MARKET_PRICE = 'regularMarketPrice'

    def __init__(self, stock_name: str) -> None:
        self.stock_name: str = stock_name
        self.stock_ticker: yf.Ticker = yf.Ticker(stock_name)

    def get_historical_data(self, period: Period) -> pd.DataFrame:
        history = self.stock_ticker.history(
            start = DateFormatter.format_date(period.start),
            end = DateFormatter.format_date(period.end)
            )
        self.df_ = pd.DataFrame(history)
        return self.df_
    
    def get_current_price(self) -> float:
        return self.stock_ticker.info[StockUtility._MARKET_PRICE]

    def save_data(self, filename: str|None = None, extension='csv') -> None:
        if filename is None:
            filename = f'{self.stock_name}_data.{extension}'

        data_dir = Path(__file__).parent.parent
        DirectoryUtil.directory_exists(data_dir, 'data', True)

        match extension:
            case 'csv': self.df_.to_csv(data_dir / 'data'/ filename) 
            case _: raise NotImplementedError('Only csv format is supported')

    def load_data(self, filename: str|None = None, extension='csv') -> None:
        if filename is None:
            filename = f'{self.stock_name}_data.{extension}'

        data_dir = Path(__file__).parent.parent
        DirectoryUtil.directory_exists(data_dir, 'data', True)

        match extension:
            case 'csv': self.df_ = pd.read_csv(data_dir / 'data'/ filename)
            case _: raise NotImplementedError('Only csv format is supported')