import pygame
import sys
from core.screen import Screen
from core.constants import FONT_TITLE_PATH, FONT_BODY_PATH

_DARK_BG     = (28, 18, 10)
_GOLD        = (255, 200, 50)
_SILVER      = (180, 180, 200)
_WHITE       = (255, 248, 240)
_RED_MUTED   = (200, 80, 80)
_GREEN_MUTED = (80, 180, 80)

_font_title  = None
_font_body   = None
_font_small  = None


def _load_fonts():
    global _font_title, _font_body, _font_small
    if _font_title is not None:
        return
    try:
        _font_title = pygame.font.Font(FONT_TITLE_PATH, 64)
        _font_body  = pygame.font.Font(FONT_BODY_PATH,  36)
        _font_small = pygame.font.Font(FONT_BODY_PATH,  24)
    except Exception:
        _font_title = pygame.font.SysFont('georgia', 64, bold=True)
        _font_body  = pygame.font.SysFont('arial', 36)
        _font_small = pygame.font.SysFont('arial', 24)


class ScoreScreen:
    def __init__(self, score_left: int, score_right: int,
                 lost_time_left: float = None, lost_time_right: float = None):
        self.screen          = Screen().screen
        self.score_left      = score_left
        self.score_right     = score_right
        self.lost_time_left  = lost_time_left
        self.lost_time_right = lost_time_right
        self.result          = None
        self.running         = True
        self.buttons         = {}

    @staticmethod
    def _fmt_time(seconds: float) -> str:
        if seconds is None:
            return "—"
        m, s = divmod(int(seconds), 60)
        return f"{m}:{s:02d}"

    def _winner(self) -> str:
        """Qui a tenu le plus longtemps (ou le plus de points si les deux ont perdu en même temps)."""
        if self.lost_time_left is None and self.lost_time_right is None:
            if self.score_left > self.score_right:
                return "Joueur 1"
            elif self.score_right > self.score_left:
                return "Joueur 2"
            return "Égalité !"
        if self.lost_time_left is None:
            return "Joueur 1"
        if self.lost_time_right is None:
            return "Joueur 2"
        if self.lost_time_left > self.lost_time_right:
            return "Joueur 1"
        if self.lost_time_right > self.lost_time_left:
            return "Joueur 2"
        # Same time — compare scores
        if self.score_left > self.score_right:
            return "Joueur 1"
        if self.score_right > self.score_left:
            return "Joueur 2"
        return "Égalité !"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.result = "quit"; self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for name, rect in self.buttons.items():
                    if rect.collidepoint(event.pos):
                        self.result = name; self.running = False

    def _draw_button(self, text: str, cx: int, cy: int) -> pygame.Rect:
        font  = _font_small
        label = font.render(text, True, _DARK_BG)
        rect  = label.get_rect(center=(cx, cy))
        pad   = pygame.Rect(rect.left - 24, rect.top - 12, rect.width + 48, rect.height + 24)
        pygame.draw.rect(self.screen, _GOLD, pad, border_radius=14)
        self.screen.blit(label, rect)
        return pad

    def draw(self):
        w, h = self.screen.get_size()
        self.screen.fill(_DARK_BG)
        _load_fonts()

        winner = self._winner()

        # ── Title
        title = _font_title.render("Fin de partie !", True, _GOLD)
        self.screen.blit(title, title.get_rect(centerx=w // 2, top=40))

        # ── Winner banner
        win_surf = _font_body.render(f"Gagnant : {winner}", True, _GOLD)
        self.screen.blit(win_surf, win_surf.get_rect(centerx=w // 2, top=130))

        # ── Separator
        pygame.draw.line(self.screen, (80, 60, 40), (60, 200), (w - 60, 200), 2)

        # ── Player columns
        col_y = 220
        for side, score, lost_t, label in [
            ("left",  self.score_left,  self.lost_time_left,  "Joueur 1"),
            ("right", self.score_right, self.lost_time_right, "Joueur 2"),
        ]:
            cx = w // 4 if side == "left" else 3 * w // 4
            is_winner = (label == winner)

            name_color = _GOLD if is_winner else _WHITE
            name_surf  = _font_body.render(label, True, name_color)
            self.screen.blit(name_surf, name_surf.get_rect(centerx=cx, top=col_y))

            score_surf = _font_body.render(f"{score} pts", True, _GREEN_MUTED if is_winner else _SILVER)
            self.screen.blit(score_surf, score_surf.get_rect(centerx=cx, top=col_y + 55))

            survived = _font_small.render(
                f"Tenu {self._fmt_time(lost_t)}" if lost_t else "Jusqu'au bout",
                True, _WHITE
            )
            self.screen.blit(survived, survived.get_rect(centerx=cx, top=col_y + 105))

        # ── Buttons
        btn_y = h - 100
        replay_rect = self._draw_button("Rejouer",  w // 2 - 130, btn_y)
        quit_rect   = self._draw_button("Quitter",  w // 2 + 130, btn_y)
        self.buttons = {"replay": replay_rect, "quit": quit_rect}

        pygame.display.flip()

    def run(self) -> str:
        while self.running:
            self.handle_events()
            self.draw()
        return self.result
