import pygame
import sys
from core.screen import Screen
from core.constants import (
    MENU_BG_COLOR, MENU_TITLE_COLOR, MENU_TITLE_FONT_SIZE,
    MENU_BTN_COLOR, MENU_BTN_HOVER_COLOR, MENU_BTN_TEXT_COLOR, MENU_BTN_SHADOW_COLOR,
    MENU_BTN_FONT_SIZE, MENU_BTN_WIDTH, MENU_BTN_HEIGHT,
    MENU_BTN_BORDER_RADIUS, MENU_BTN_SHADOW_OFFSET, MENU_BTN_SPACING,
)


class PlayerSelectScreen:
    """Screen shown after clicking Play — lets the user choose who controls each side."""

    # Returned values
    TWO_PLAYERS  = "two_players"
    P1_VS_BOT    = "p1_vs_bot"
    BOT_VS_P2    = "bot_vs_p2"

    def __init__(self):
        self.screen  = Screen().screen
        self.running = True
        self.result  = None
        self.buttons = {}

    def _draw_button(self, label: str, key: str, x: int, y: int):
        rect = pygame.Rect(x, y, MENU_BTN_WIDTH, MENU_BTN_HEIGHT)
        self.buttons[key] = rect
        is_hovered = rect.collidepoint(pygame.mouse.get_pos())

        shadow = rect.move(MENU_BTN_SHADOW_OFFSET, MENU_BTN_SHADOW_OFFSET)
        pygame.draw.rect(self.screen, MENU_BTN_SHADOW_COLOR, shadow, border_radius=MENU_BTN_BORDER_RADIUS)

        color = MENU_BTN_HOVER_COLOR if is_hovered else MENU_BTN_COLOR
        pygame.draw.rect(self.screen, color, rect, border_radius=MENU_BTN_BORDER_RADIUS)

        font = pygame.font.SysFont(None, MENU_BTN_FONT_SIZE)
        surf = font.render(label, True, MENU_BTN_TEXT_COLOR)
        self.screen.blit(surf, surf.get_rect(center=rect.center))

    def draw(self):
        self.screen.fill(MENU_BG_COLOR)
        cx     = self.screen.get_width()  // 2
        btn_x  = cx - MENU_BTN_WIDTH // 2
        base_y = self.screen.get_height() // 2 - MENU_BTN_SPACING

        font_title = pygame.font.SysFont(None, MENU_TITLE_FONT_SIZE)
        title = font_title.render("Choisir les joueurs", True, MENU_TITLE_COLOR)
        self.screen.blit(title, title.get_rect(center=(cx, base_y - 80)))

        self._draw_button("2 Joueurs",       self.TWO_PLAYERS, btn_x, base_y)
        self._draw_button("Joueur 1 + IA",   self.P1_VS_BOT,   btn_x, base_y + MENU_BTN_SPACING)
        self._draw_button("IA + Joueur 2",   self.BOT_VS_P2,   btn_x, base_y + MENU_BTN_SPACING * 2)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for key, rect in self.buttons.items():
                    if rect.collidepoint(event.pos):
                        self.result  = key
                        self.running = False

    def run(self) -> str | None:
        while self.running:
            self.handle_events()
            self.draw()
        return self.result
