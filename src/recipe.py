from dataclasses import dataclass
from enums import Ingredient, CakeType

@dataclass(frozen=True)
class Recipe:
    cake_type:   CakeType
    ingredients: tuple[Ingredient, ...]  # tuple = immutable, hashable
    reward:      int                     # score points rewarded on completion
    time_limit:  float                   # seconds the customer will wait
