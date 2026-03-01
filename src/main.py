import pygame
import sys
import os
# Ensure src/ is always on the path (robustness when run from any directory)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.menu import Menu
from game.run import Game
from core.enums import MenuButton

def main():
    pygame.init()

    result = Menu().run()

    if result == MenuButton.JOUER:
        Game().run()
    elif result == MenuButton.SCORE:
        pass  # TODO: leaderboard screen

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
