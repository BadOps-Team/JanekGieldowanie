from dataclasses import dataclass
import random
import numpy as np
from typing import Self

@dataclass
class Gene:
    content: list[float]

    @staticmethod
    def mutate_float(value: float, settings) -> float:
        return value + float(np.random.normal(0, settings.float_mutation_variance))

    def mutate_change(self, settings):
        i = random.randrange(len(self.content))
        self.content[i] = self.mutate_float(self.content[i], settings)

    def mutate_rotate(self, settings):
        new_content = self.content.copy()
        start = random.randrange(len(self.content))
        size = int(np.random.lognormal(0, settings.rotation_size_variance))
        shift = int(np.random.lognormal(0, settings.rotation_shift_variance))
        if size == 1:
            return

        for i in range(size):
            cur_pos = (start+i) % len(self.content)
            target_pos = (cur_pos+shift) % len(self.content)
            if i >= size-shift:
                target_pos = (target_pos+len(self.content)-size) % len(self.content)

            new_content[cur_pos] = self.content[target_pos]

        self.content = new_content

    def mutate(self, settings):
        if np.random.random() < settings.mutate_change_chance:
            self.mutate_change(settings)
        if np.random.random() < settings.mutate_rotate_chance:
            self.mutate_rotate(settings)

    def crossover_point(self, other: Self, settings) -> Self:
        child1 = self.content
        child2 = other.content
        for _ in range(settings.crossover_point_amount):
            point = random.randrange(len(self.content))

            left1 = child1[:point]
            right1 = child1[point:]
            left2 = child2[:point]
            right2 = child2[point:]

            child1 = left1 + right2
            child2 = left2 + right1

        return Gene(child1) if random.random() < 0.5 else Gene(child2)

    @staticmethod
    def crossover_float(float1: float, float2: float, settings) -> float:
        beta = np.random.uniform(-settings.crossover_imbalance, 1+settings.crossover_imbalance)
        return float1*beta + float2*(1-beta)

    def crossover_uniform(self, other: Self, settings) -> Self:
        new_gene = Gene([0 for _ in range(len(self.content))])
        for i in range(len(self.content)):
            new_gene.content[i] = self.crossover_float(self.content[i], other.content[i], settings)

        return new_gene

    def crossover(self, other: Self, settings) -> Self:
        if random.random() < settings.crossover_point_chance:
            return self.crossover_point(other, settings)
        else:
            return self.crossover_uniform(other, settings)
