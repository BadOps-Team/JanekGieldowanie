from dataclasses import dataclass

@dataclass
class GASettings:
    children_ratio: float = 0.3
    crossover_imbalance: float = 0.25
    float_mutation_variance: float = 0.1
    rotation_size_variance: float = 1
    rotation_shift_variance: float = 1
    mutate_change_chance: float = 0.5
    mutate_rotate_chance: float = 0.5
    crossover_point_amount: int = 2
    crossover_point_chance: float = 0.5