from Stocks.stock_price_estimator import *
from Stocks.stock_utility import StockUtility
from enum import Enum
from typing import Self

class EstimatorStrategy(Enum):
    METHOD_OF_MOMENTS = 1
    MAXIMUM_LIKELIHOOD = 2
    LEAST_SQUARE_METHOD = 3

class EstimatorBuilder:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def create_builder() -> Self:
        return EstimatorBuilder()

    def with_startegy(self, strategy: EstimatorStrategy) -> Self:
        self.strategy_ = strategy
        return self
    
    def with_stock_util(self, stock_util: StockUtility) -> Self:
        self.stock_util_ = stock_util
        return self
    
    def build(self) -> StockPriceEstimator:
        match self.strategy_:
            case EstimatorStrategy.METHOD_OF_MOMENTS:
                return MethodOfMomentsEstimator(self.stock_util_)
            case EstimatorStrategy.MAXIMUM_LIKELIHOOD:
                return MaximumLikelihoodEstimator(self.stock_util_)
            case EstimatorStrategy.LEAST_SQUARE_METHOD:
                return LeastSqaureMethodEstimator(self.stock_util_)
            case _:
                raise NotImplementedError()