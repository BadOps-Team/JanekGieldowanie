from .stock_utility import StockUtility
from .estimators import EstimatorStrategy, EstimatorBuilder
import json

class StockUtilityFactory:
    def __init__(self, strategy: EstimatorStrategy, config_file_path: str) -> None:
        self.strategy = strategy

        # init config
        with open(config_file_path, 'r', encoding='utf-8-sig') as f: # Added encoding='utf-8-sig'
            json_config = json.load(f)
            StockUtility.create_config(json_config)

    def create_stock_utilty(self, stock_name: str) -> StockUtility:
        estimator = (EstimatorBuilder
                    .create_builder()
                    .with_startegy(self.strategy)
                    .build())
        
        stock =  StockUtility(stock_name, estimator)
        return stock

