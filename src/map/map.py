import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from screen import Screen
from constants import MAP_BG_COLOR, MAP_SEPARATOR_COLOR, MAP_SEPARATOR_WIDTH, MAP_KITCHEN_RATIO, PLAYER_SPEED, FPS, TIME_FAST_FORWARD_SCALE
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

    def update(self, dt: float):
        self.zone_left.update(dt)
        self.zone_right.update(dt)

    def _time_scale(self) -> float:
        """Returns a time multiplier — hold TAB to fast-forward."""
        keys = pygame.key.get_pressed()
        return TIME_FAST_FORWARD_SCALE if keys[pygame.K_TAB] else 1.0

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0 * self._time_scale()
            self.handle_events()
            self.update(dt)
            self.draw()
