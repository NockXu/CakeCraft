import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from menu import Menu
from map.map import Map
from enums import MenuButton

def main():
    pygame.init()

    result = Menu().run()

    if result == MenuButton.JOUER:
        Map().run()
    elif result == MenuButton.SCORE:
        print("You have pressed Score")
        pass  # TODO: Score screen

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
