from enum import Enum

class MenuButton(Enum):
    JOUER = "Jouer"
    SCORE = "Score"
    QUITTER = "Quitter"

class Side(Enum):
    LEFT = "left"
    RIGHT = "right"