from abc import ABC
import yfinance as yf
from .estimation_result import EstimationResult
import numpy as np

class StockPriceEstimator(ABC):
    def __init__(self) -> None:
        pass

    def estimate_from_historic(self, historic_close_prices: np.ndarray, future_days: int) -> EstimationResult:
        pass

class LeastSqaureMethodEstimator(StockPriceEstimator):
    def __init__(self) -> None:
        super().__init__()

    def estimate_from_historic(self, historic_close_prices: np.ndarray, future_days: int) -> EstimationResult:
        n = len(historic_close_prices)
        X = np.linspace(0, 1, n).reshape(-1, 1)
        y = historic_close_prices.values.reshape(-1, 1)
        
        X_with_intercept = np.hstack([np.ones((n, 1)), X])
        coefficients = np.linalg.inv(X_with_intercept.T @ X_with_intercept) @ X_with_intercept.T @ y
        
        a = coefficients[0, 0]
        b = coefficients[1, 0]
        
        future_X = np.linspace(1, 1 + future_days/n, future_days).reshape(-1, 1)
        predictions = a + b * future_X
        
        return EstimationResult(predictions.flatten(), (a, b))
    
class MethodOfMomentsEstimator(StockPriceEstimator):
    def __init__(self) -> None:
        super().__init__()

    def estimate_from_historic(self, historic_close_prices: np.ndarray, future_days: int) -> EstimationResult:
        returns = np.diff(historic_close_prices) / historic_close_prices[:-1]
        
        mu = np.mean(returns)
        sigma = np.std(returns)
        
        last_price = historic_close_prices.iloc[-1]
        predictions = [
            last_price * (1 + mu) ** day for day in range(1, future_days + 1)
        ]
        
        return EstimationResult(np.array(predictions), (mu, sigma))
    
class MaximumLikelihoodEstimator(StockPriceEstimator):
    def __init__(self) -> None:
        super().__init__()

    def estimate_from_historic(self, historic_close_prices: np.ndarray, future_days: int) -> EstimationResult:
        log_returns = np.diff(np.log(historic_close_prices))
        
        mu = np.mean(log_returns) 
        sigma = np.std(log_returns)
        
        last_price = historic_close_prices.iloc[-1]
        mean_prediction = last_price * np.exp(mu * np.arange(1, future_days + 1))

        return EstimationResult(mean_prediction, (mu, sigma))