from Stocks import StockUtilityFactory 
from Stocks.estimators import EstimatorStrategy
from Stocks import Period
from .test_config import TEST_ESTIMATOR_CONFIGS
from math import floor
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


class EstimatorsTests:
    def __init__(self):
        n  = len(TEST_ESTIMATOR_CONFIGS)
        self.results = {
            EstimatorStrategy.LEAST_SQUARE_METHOD: [[] for _ in range(n)],
            EstimatorStrategy.METHOD_OF_MOMENTS: [[] for _ in range(n)],
            EstimatorStrategy.MAXIMUM_LIKELIHOOD: [[] for _ in range(n)]
        }

    def run_tests(self):
        for idx, config in enumerate(TEST_ESTIMATOR_CONFIGS):
            self.run_test(config, EstimatorStrategy.LEAST_SQUARE_METHOD, idx)
            self.run_test(config, EstimatorStrategy.METHOD_OF_MOMENTS, idx)
            self.run_test(config, EstimatorStrategy.MAXIMUM_LIKELIHOOD, idx)

    def run_test(self, config, strategy, i):
        factory = StockUtilityFactory(strategy, config)
        stock_utility = factory.create_stock_utilty("AAPL")
        period = Period(config['start_date'], config['end_date'])
        historical_prices = stock_utility.get_historical_close_prices(period).tolist()

        n = len(historical_prices)

        checkpoints = (
            0, 
            floor(n * 1 / 3), 
            floor(n * 2 / 3), 
            n - config['forecast_days'] - 1
        )

        diffs = []
        result = stock_utility.get_estimations()
        
        fig, ax1 = plt.subplots(figsize=(14, 8))
        
        ax1.plot(range(n), historical_prices, 'b-', linewidth=2, label='Historical Prices')
        ax1.set_xlabel('Time (days)')
        ax1.set_ylabel('Stock Price', color='b')
        ax1.tick_params(axis='y', labelcolor='b')
        
        ax2 = ax1.twinx()
        error_line, = ax2.plot([], [], 'r-', linewidth=2, label='Squared Errors')
        ax2.set_ylabel('Squared Error', color='r')
        ax2.tick_params(axis='y', labelcolor='r')
        
        trend_colors = ['g', 'm', 'c', 'y']
        checkpoint_labels = ['Start', '1/3 Period', '2/3 Period', 'End']
        
        for idx, res in enumerate(result):
            diff_days = idx + config['forecast_days']
            if len(res.estimated_prices) != len(historical_prices[idx:diff_days]):
                continue
            total_diff = np.sum((res.estimated_prices - historical_prices[idx:diff_days]) ** 2)
            diffs.append(total_diff)
            
            if idx in checkpoints:
                cp_idx = checkpoints.index(idx)
                print(f"Checkpoint {checkpoint_labels[cp_idx]}: {res.estimated_prices}")
                
                a, b = res.equation_coefficients
                x_trend = np.array([idx, n-1])
                y_trend = a + b * x_trend
                ax1.plot(x_trend, y_trend, 
                        color=trend_colors[cp_idx], 
                        linestyle='--',
                        linewidth=1.5,
                        label=f'Trend @ {checkpoint_labels[cp_idx]}')
                
                ax1.axvline(x=idx, color=trend_colors[cp_idx], alpha=0.3)
        
        error_line.set_data(range(len(diffs)), diffs)
        ax2.relim()
        ax2.autoscale_view()
        
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        plt.title(f'{strategy.name}: Prices, Errors & Trend Lines')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        path = Path(__file__).parent
        plt.savefig(path / "results" / f"{strategy.name}_test_{i}.png")
        
        self.results[strategy][i] = diffs