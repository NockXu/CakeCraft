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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        # Continuous key press for movement
        keys = pygame.key.get_pressed()

        # Player 1 — ZQSD
        p1 = self.zone_left.player
        if keys[pygame.K_q]:
            p1.move(-PLAYER_SPEED, 0)
        if keys[pygame.K_d]:
            p1.move(PLAYER_SPEED, 0)
        if keys[pygame.K_z]:
            p1.move(0, -PLAYER_SPEED)
        if keys[pygame.K_s]:
            p1.move(0, PLAYER_SPEED)

        # Player 2 — Arrow keys
        p2 = self.zone_right.player
        if keys[pygame.K_LEFT]:
            p2.move(-PLAYER_SPEED, 0)
        if keys[pygame.K_RIGHT]:
            p2.move(PLAYER_SPEED, 0)
        if keys[pygame.K_UP]:
            p2.move(0, -PLAYER_SPEED)
        if keys[pygame.K_DOWN]:
            p2.move(0, PLAYER_SPEED)

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

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
