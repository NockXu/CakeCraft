import pygame
import sys
from game.map import Map
from core.constants import FPS, TIME_FAST_FORWARD_SCALE
from game.event_handler import eventHandler


class Game:
    def __init__(self, bot_left: bool = False, bot_right: bool = False):
        pygame.init()
        self._bot_left    = bot_left
        self._bot_right   = bot_right
        self.map          = Map(bot_left=bot_left, bot_right=bot_right)
        self.eventHandler = eventHandler()
        self.eventHandler.add_thing(self.map.zone_left)
        self.eventHandler.add_thing(self.map.zone_right)
        self.clock   = pygame.time.Clock()
        self.running = True

    def _time_scale(self) -> float:
        keys = pygame.key.get_pressed()
        return TIME_FAST_FORWARD_SCALE if keys[pygame.K_TAB] else 1.0

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0 * self._time_scale()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    else:
                        self.eventHandler.handle_keydown(event.key)

            keys = pygame.key.get_pressed()
            self.eventHandler.handle_movement(keys)
            self.eventHandler.handle_events()

            self.map.update(dt)
            self.map.draw()

            if self.map.game_over:
                self.running = False

        # Show score screen when game ends (not on escape)
        if self.map.game_over:
            self._show_score_screen()

        pygame.quit()
        sys.exit()

    def _show_score_screen(self):
        from game.score_screen import ScoreScreen
        result = ScoreScreen(
            score_left      = self.map.zone_left.score,
            score_right     = self.map.zone_right.score,
            lost_time_left  = self.map.zone_left.lost_time,
            lost_time_right = self.map.zone_right.lost_time,
        ).run()
        if result == "replay":
            self.map     = Map(bot_left=self._bot_left, bot_right=self._bot_right)
            self.running = True
            self.run()
