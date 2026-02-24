from enum import Enum

class MenuButton(Enum):
    JOUER = "Jouer"
    SCORE = "Score"
    QUITTER = "Quitter"

class Side(Enum):
    LEFT = "left"
    RIGHT = "right"

class Ingredient(Enum):
    FLOUR       = "Farine"
    EGG         = "Oeuf"
    BUTTER      = "Beurre"
    SUGAR       = "Sucre"
    CREAM       = "Crème"
    CHOCOLATE   = "Chocolat"
    STRAWBERRY  = "Fraise"
    VANILLA     = "Vanille"

class CakeType(Enum):
    VANILLA_CAKE    = "Gâteau Vanille"
    CHOCOLATE_CAKE  = "Gâteau Chocolat"
    STRAWBERRY_CAKE = "Gâteau Fraise"
    CREAM_PUFF      = "Chou à la Crème"

class CustomerState(Enum):
    WALKING  = "walking"   # moving toward their spot in line
    QUEUED   = "queued"    # standing in line, not at front — no timer
    WAITING  = "waiting"   # at the front of the counter — patience decreasing
    SERVED   = "served"    # order fulfilled, leaving happily
    LEAVING  = "leaving"   # patience ran out, leaving angry