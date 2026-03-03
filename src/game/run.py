import pygame
from game.map import Map
from core.constants import FPS, TIME_FAST_FORWARD_SCALE
from game.event_handler import eventHandler


class Game:
    def __init__(self, bot_left: bool = False, bot_right: bool = False):
        pygame.init()
        self._bot_left    = bot_left
        self._bot_right   = bot_right
        self._vs_mode     = not bot_left and not bot_right  # true 1v1
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
        self._spectating   = False  # human lost but is watching the bot
        self._human_died   = False  # human lost (quit or spectate)

        while self.running:
            dt = self.clock.tick(FPS) / 1000.0 * self._time_scale()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_6):
                        self.running = False
                    elif not self._spectating:
                        self.eventHandler.handle_keydown(event.key)

            if not self._spectating:
                keys = pygame.key.get_pressed()
                self.eventHandler.handle_movement(keys)
                self.eventHandler.handle_events()

            self.map.update(dt)
            self.map.draw()

            if self.map.game_over:
                self.running = False
            elif not self._spectating and not self._human_died and self._human_just_lost():
                self._human_died = True
                choice = self._ask_spectate_or_quit()
                if choice == "quit":
                    self.running = False
                else:
                    self._spectating = True

        # Show score screen when game ends naturally (not ESC)
        if self.map.game_over or self._human_died:
            self._show_score_screen(self._vs_mode, self._bot_left, self._bot_right)

    def _human_just_lost(self) -> bool:
        """True when the human side has just exhausted all lives (J vs bot only)."""
        if self._vs_mode:
            return False
        if self._bot_right and self.map.zone_left.has_lost():
            return True
        if self._bot_left and self.map.zone_right.has_lost():
            return True
        return False

    def _ask_spectate_or_quit(self) -> str:
        """Show a small overlay asking the human player to quit or spectate."""
        screen  = self.map.screen
        w, h    = screen.get_size()
        font_b  = pygame.font.SysFont("arial", 32, bold=True)
        font_s  = pygame.font.SysFont("arial", 22)
        clock   = pygame.time.Clock()

        btn_quit = pygame.Rect(w // 2 - 200, h // 2 + 20, 160, 50)
        btn_spec = pygame.Rect(w // 2 + 40,  h // 2 + 20, 200, 50)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_6):
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if btn_quit.collidepoint(event.pos):
                        return "quit"
                    if btn_spec.collidepoint(event.pos):
                        return "spectate"

            # Dim overlay
            overlay = pygame.Surface((w, h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            msg = font_b.render("Vous avez perdu !", True, (255, 200, 50))
            screen.blit(msg, msg.get_rect(centerx=w // 2, centery=h // 2 - 30))

            pygame.draw.rect(screen, (180, 60, 60),  btn_quit, border_radius=10)
            pygame.draw.rect(screen, (60, 120, 180), btn_spec, border_radius=10)
            screen.blit(font_s.render("Quitter", True, (255,255,255)),
                        font_s.render("Quitter", True, (255,255,255)).get_rect(center=btn_quit.center))
            screen.blit(font_s.render("Regarder la suite", True, (255,255,255)),
                        font_s.render("Regarder la suite", True, (255,255,255)).get_rect(center=btn_spec.center))

            pygame.display.flip()
            clock.tick(60)

    def _show_score_screen(self, vs_mode: bool, bot_left: bool, bot_right: bool):
        from game.score_screen import ScoreScreen
        result = ScoreScreen(
            score_left      = self.map.zone_left.score,
            score_right     = self.map.zone_right.score,
            lost_time_left  = self.map.zone_left.lost_time,
            lost_time_right = self.map.zone_right.lost_time,
            vs_mode         = vs_mode,
            bot_left        = bot_left,
            bot_right       = bot_right,
        ).run()
        if result == "replay":
            self.map     = Map(bot_left=self._bot_left, bot_right=self._bot_right)
            self.running = True
            self.run()
