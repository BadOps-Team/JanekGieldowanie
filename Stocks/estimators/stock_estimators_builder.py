from .stock_price_estimator import *
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
    
    def build(self) -> StockPriceEstimator:
        match self.strategy_:
            case EstimatorStrategy.METHOD_OF_MOMENTS:
                return MethodOfMomentsEstimator()
            case EstimatorStrategy.MAXIMUM_LIKELIHOOD:
                return MaximumLikelihoodEstimator()
            case EstimatorStrategy.LEAST_SQUARE_METHOD:
                return LeastSqaureMethodEstimator()
            case _:
                raise NotImplementedError()