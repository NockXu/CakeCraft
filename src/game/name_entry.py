import pygame
import sys
from core.screen import Screen

_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_NAME_LEN = 3

_DARK_BG  = (28, 18, 10)
_GOLD     = (255, 200, 50)
_WHITE    = (255, 248, 240)
_GREY     = (120, 110, 100)
_RED      = (200, 80, 80)
_GREEN    = (80, 200, 80)

# J1: arrows + button 3 (confirm letter) + button 4 (validate name)
_J1_UP      = pygame.K_UP
_J1_DOWN    = pygame.K_DOWN
_J1_CONFIRM = pygame.K_3
_J1_SUBMIT  = pygame.K_4

# J2: o=up, l=down + e (confirm letter) + q (validate name)
_J2_UP      = pygame.K_o
_J2_DOWN    = pygame.K_l
_J2_CONFIRM = pygame.K_e
_J2_SUBMIT  = pygame.K_q


class _PlayerPicker:
    """State for one player's 3-letter picker."""
    def __init__(self, key_up, key_down, key_confirm, key_submit):
        self.key_up      = key_up
        self.key_down    = key_down
        self.key_confirm = key_confirm
        self.key_submit  = key_submit
        self.letters     = [0] * _NAME_LEN
        self.cursor      = 0
        self.done        = False
        self.skipped     = False

    @property
    def result(self):
        return None if self.skipped else "".join(_ALPHABET[i] for i in self.letters)

    def handle_key(self, key):
        if self.done:
            return
        if key == self.key_up:
            self.letters[self.cursor] = (self.letters[self.cursor] - 1) % len(_ALPHABET)
        elif key == self.key_down:
            self.letters[self.cursor] = (self.letters[self.cursor] + 1) % len(_ALPHABET)
        elif key == self.key_confirm:
            if self.cursor < _NAME_LEN - 1:
                self.cursor += 1
            else:
                self.done = True
        elif key == self.key_submit:
            self.done = True
        elif key in (pygame.K_ESCAPE, pygame.K_6):
            self.skipped = True
            self.done    = True


def _draw_picker(screen, picker: _PlayerPicker, cx: int, top_y: int,
                 font_big, font_small, label: str, color_label, done_color):
    """Draw one player's picker centered at cx, starting at top_y."""
    # Label (e.g. "Joueur 1")
    lbl = font_small.render(label, True, color_label)
    screen.blit(lbl, lbl.get_rect(centerx=cx, top=top_y))

    if picker.done and not picker.skipped:
        # Show validated name in green
        name = "".join(_ALPHABET[i] for i in picker.letters)
        surf = font_big.render(name, True, done_color)
        screen.blit(surf, surf.get_rect(centerx=cx, top=top_y + 34))
        ok = font_small.render("OK ✓", True, done_color)
        screen.blit(ok, ok.get_rect(centerx=cx, top=top_y + 34 + surf.get_height() + 4))
        return
    elif picker.done and picker.skipped:
        surf = font_small.render("(ignoré)", True, _RED)
        screen.blit(surf, surf.get_rect(centerx=cx, top=top_y + 34))
        return

    slot_w = 72
    gap    = 14
    total_w = _NAME_LEN * slot_w + (_NAME_LEN - 1) * gap
    start_x = cx - total_w // 2
    slot_y  = top_y + 34

    for i in range(_NAME_LEN):
        sx   = start_x + i * (slot_w + gap)
        rect = pygame.Rect(sx, slot_y, slot_w, 76)
        col  = _GOLD if i == picker.cursor else _GREY
        pygame.draw.rect(screen, col, rect, 3, border_radius=8)

        letter = _ALPHABET[picker.letters[i]]
        lsurf  = font_big.render(letter, True, _WHITE if i == picker.cursor else _GREY)
        screen.blit(lsurf, lsurf.get_rect(center=rect.center))

        if i == picker.cursor:
            arr_u = font_small.render("▲", True, _GOLD)
            arr_d = font_small.render("▼", True, _GOLD)
            screen.blit(arr_u, arr_u.get_rect(centerx=rect.centerx, bottom=rect.top - 2))
            screen.blit(arr_d, arr_d.get_rect(centerx=rect.centerx, top=rect.bottom + 2))


class NameEntry:
    """Single-player name entry (kept for solo/bot modes)."""

    def __init__(self, player_index: int, prompt: str):
        self.screen       = Screen().screen
        self.player_index = player_index
        self.prompt       = prompt
        self._font_big    = pygame.font.SysFont("monospace", 72, bold=True)
        self._font_mid    = pygame.font.SysFont("monospace", 36)
        self._font_small  = pygame.font.SysFont("monospace", 20)

        if player_index == 0:
            self._picker = _PlayerPicker(_J1_UP, _J1_DOWN, _J1_CONFIRM, _J1_SUBMIT)
            self._hint   = "Haut/Bas: changer  |  [3]: confirmer lettre  |  [4]: valider"
        else:
            self._picker = _PlayerPicker(_J2_UP, _J2_DOWN, _J2_CONFIRM, _J2_SUBMIT)
            self._hint   = "O/L: changer  |  [E]: confirmer lettre  |  [Q]: valider"

    def _draw(self):
        w, h = self.screen.get_size()
        self.screen.fill(_DARK_BG)

        surf = self._font_mid.render(self.prompt, True, _GOLD)
        self.screen.blit(surf, surf.get_rect(centerx=w // 2, top=h // 2 - 180))

        hint_surf = self._font_small.render(self._hint, True, _GREY)
        self.screen.blit(hint_surf, hint_surf.get_rect(centerx=w // 2, top=h // 2 - 130))

        skip_surf = self._font_small.render("ECHAP / [6]: passer (score non sauvegarde)", True, _RED)
        self.screen.blit(skip_surf, skip_surf.get_rect(centerx=w // 2, top=h // 2 - 104))

        _draw_picker(self.screen, self._picker, w // 2, h // 2 - 60,
                     self._font_big, self._font_small, "", _GOLD, _GREEN)
        pygame.display.flip()

    def run(self) -> str | None:
        clock = pygame.time.Clock()
        while not self._picker.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._picker.handle_key(event.key)
            self._draw()
            clock.tick(60)
        return self._picker.result


class NameEntryDuo:
    """Both players enter their name simultaneously."""

    def __init__(self):
        self.screen      = Screen().screen
        self._font_big   = pygame.font.SysFont("monospace", 64, bold=True)
        self._font_mid   = pygame.font.SysFont("monospace", 28)
        self._font_small = pygame.font.SysFont("monospace", 18)

        self._p1 = _PlayerPicker(_J1_UP, _J1_DOWN, _J1_CONFIRM, _J1_SUBMIT)
        self._p2 = _PlayerPicker(_J2_UP, _J2_DOWN, _J2_CONFIRM, _J2_SUBMIT)

    def _draw(self):
        w, h = self.screen.get_size()
        self.screen.fill(_DARK_BG)

        title = self._font_mid.render("Entrez vos noms !", True, _GOLD)
        self.screen.blit(title, title.get_rect(centerx=w // 2, top=30))

        # Hints
        h1 = self._font_small.render("J1 — Haut/Bas: changer  [3]: lettre suivante  [4]: valider", True, _GREY)
        h2 = self._font_small.render("J2 — O/L: changer  [E]: lettre suivante  [Q]: valider", True, _GREY)
        skip = self._font_small.render("ECHAP / [6]: passer (score non sauvegarde)", True, _RED)
        self.screen.blit(h1,   h1.get_rect(centerx=w // 2, top=76))
        self.screen.blit(h2,   h2.get_rect(centerx=w // 2, top=100))
        self.screen.blit(skip, skip.get_rect(centerx=w // 2, top=124))

        cx1 = w // 4
        cx2 = 3 * w // 4
        top = h // 2 - 80

        _draw_picker(self.screen, self._p1, cx1, top,
                     self._font_big, self._font_small, "Joueur 1", _GOLD, _GREEN)
        _draw_picker(self.screen, self._p2, cx2, top,
                     self._font_big, self._font_small, "Joueur 2", (100, 160, 255), _GREEN)

        # Separator
        pygame.draw.line(self.screen, _GREY, (w // 2, 160), (w // 2, h - 60), 1)

        pygame.display.flip()

    def run(self) -> tuple[str | None, str | None]:
        """Returns (name1, name2); None means skipped."""
        clock = pygame.time.Clock()
        while not (self._p1.done and self._p2.done):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._p1.handle_key(event.key)
                    self._p2.handle_key(event.key)
            self._draw()
            clock.tick(60)
        return self._p1.result, self._p2.result
