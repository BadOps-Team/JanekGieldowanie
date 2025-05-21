from .period import Period
from Util import DateFormatter, DirectoryUtil
from .estimators import StockPriceEstimator
from ._estimation_config import EstimationConfig
from pathlib import Path
import pandas as pd
import yfinance as yf


class StockUtility:
    _ESTIMATION_CONFIG = EstimationConfig

    def __init__(self, stock_name: str, estimator: StockPriceEstimator) -> None:
        self.stock_name: str = stock_name
        self.stock_ticker: yf.Ticker = yf.Ticker(stock_name)
        self.estimator = estimator

    def get_historical_close_prices(self, period: Period) -> pd.DataFrame:
        history = self.stock_ticker.history(
            start = DateFormatter.format_date(period.start),
            end = DateFormatter.format_date(period.end)
            )
        self.df_ = pd.DataFrame(history)
        return self.df_.Close

    def get_estimations(self):
        data_period = StockUtility._ESTIMATION_CONFIG.data_period()
        data = self.get_historical_close_prices(data_period)

        # adjust for weekends
        for i in StockUtility._ESTIMATION_CONFIG.estimation_range(len(data)):
            window_start = i
            window_end = i + StockUtility._ESTIMATION_CONFIG.lookback_days
            estimation_data = data.iloc[window_start:window_end]
            estimation_results = self.estimator.estimate_from_historic(
                estimation_data, 
                StockUtility._ESTIMATION_CONFIG.forecast_days
            )
            yield estimation_results
    
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

    @staticmethod
    def create_config(json_content: str) -> None:
        StockUtility._ESTIMATION_CONFIG = EstimationConfig.from_json(json_content=json_content)