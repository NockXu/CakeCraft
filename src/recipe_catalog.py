import random
from enums import Ingredient, CakeType
from recipe import Recipe

class RecipeCatalog:
    """Single source of truth for all recipes in the game.
    Add a new cake by adding an entry to _recipes — no other file needs to change.
    """

    _recipes: dict[CakeType, Recipe] = {
        CakeType.VANILLA_CAKE: Recipe(
            cake_type   = CakeType.VANILLA_CAKE,
            ingredients = (Ingredient.FLOUR, Ingredient.EGG, Ingredient.BUTTER, Ingredient.SUGAR, Ingredient.VANILLA),
            reward      = 100,
            time_limit  = 60.0,
        ),
        CakeType.CHOCOLATE_CAKE: Recipe(
            cake_type   = CakeType.CHOCOLATE_CAKE,
            ingredients = (Ingredient.FLOUR, Ingredient.EGG, Ingredient.BUTTER, Ingredient.SUGAR, Ingredient.CHOCOLATE),
            reward      = 120,
            time_limit  = 55.0,
        ),
        CakeType.STRAWBERRY_CAKE: Recipe(
            cake_type   = CakeType.STRAWBERRY_CAKE,
            ingredients = (Ingredient.FLOUR, Ingredient.EGG, Ingredient.BUTTER, Ingredient.SUGAR, Ingredient.STRAWBERRY, Ingredient.CREAM),
            reward      = 150,
            time_limit  = 50.0,
        ),
        CakeType.CREAM_PUFF: Recipe(
            cake_type   = CakeType.CREAM_PUFF,
            ingredients = (Ingredient.FLOUR, Ingredient.EGG, Ingredient.BUTTER, Ingredient.CREAM),
            reward      = 80,
            time_limit  = 45.0,
        ),
    }

    @classmethod
    def get(cls, cake_type: CakeType) -> Recipe:
        return cls._recipes[cake_type]

    @classmethod
    def random(cls) -> Recipe:
        return random.choice(list(cls._recipes.values()))

    @classmethod
    def all(cls) -> list[Recipe]:
        return list(cls._recipes.values())
