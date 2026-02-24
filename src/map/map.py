import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from screen import Screen
from constants import MAP_BG_COLOR, MAP_SEPARATOR_COLOR, MAP_SEPARATOR_WIDTH, MAP_KITCHEN_RATIO, PLAYER_SPEED, FPS
from player_zone import PlayerZone
from enums import Side

class Map:
    def __init__(self):
        self.screen: pygame.Surface = Screen().screen
        self.running = True
        self.zone_left  = PlayerZone(self.screen, Side.LEFT)
        self.zone_right = PlayerZone(self.screen, Side.RIGHT)
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.fill(MAP_BG_COLOR)

        # VERTICAL separator (left/right)
        center_x = self.screen.get_width() // 2
        pygame.draw.line(self.screen, MAP_SEPARATOR_COLOR, (center_x, 0), (center_x, self.screen.get_height()), MAP_SEPARATOR_WIDTH)

        # HORIZONTAL separator (kitchen/shop)
        kitchen_y = int(self.screen.get_height() * MAP_KITCHEN_RATIO)
        pygame.draw.line(self.screen, MAP_SEPARATOR_COLOR, (0, kitchen_y), (self.screen.get_width(), kitchen_y), MAP_SEPARATOR_WIDTH)

        # PLAYER ZONES
        self.zone_left.draw()
        self.zone_right.draw()

        pygame.display.flip()

    def update(self, dt: float):
        self.zone_left.update(dt)
        self.zone_right.update(dt)
