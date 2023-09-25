from enum import Enum


class FeeTier(Enum):
    MAX = 1 / 100
    MEDIUM = 0.3 / 100
    LOW = 0.05 / 100
