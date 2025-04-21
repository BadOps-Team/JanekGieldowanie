from dataclasses import dataclass
import numpy as np

@dataclass
class EstimationResult:
    estimated_prices: np.array
    equation_coefficients: tuple[np.float32, np.float32]