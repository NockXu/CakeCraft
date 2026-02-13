import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from screen import Screen
from constants import (
    MENU_BG_COLOR, MENU_TITLE_COLOR, MENU_TITLE_FONT_SIZE, MENU_TITLE_Y_OFFSET,
    MENU_BTN_COLOR, MENU_BTN_TEXT_COLOR, MENU_BTN_FONT_SIZE,
    MENU_BTN_WIDTH, MENU_BTN_HEIGHT, MENU_BTN_BORDER_RADIUS
)
from enums import MenuButton

class Menu:
    def __init__(self):
        self.screen: pygame.Surface = Screen().screen
        self.running = True
        self.next_screen: MenuButton | None = None
        self.buttons: dict[str, pygame.Rect] = {}

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for spec, rect in self.buttons.items():
                    if rect.collidepoint(event.pos):
                        if spec == MenuButton.JOUER:
                            self.next_screen = MenuButton.JOUER
                            self.running = False

                        elif spec == MenuButton.SCORE:
                            self.next_screen = MenuButton.SCORE
                            self.running = False

                        elif spec == MenuButton.QUITTER:
                            pygame.quit()
                            sys.exit()
                            

    def draw_button(self, spec: MenuButton, x: int, y: int, width: int, height: int):
        rect = pygame.Rect(x, y, width, height)
        self.buttons[spec] = rect
        pygame.draw.rect(self.screen, MENU_BTN_COLOR, rect, border_radius=MENU_BTN_BORDER_RADIUS)
        font = pygame.font.SysFont(None, MENU_BTN_FONT_SIZE)
        label = font.render(spec.value, True, MENU_BTN_TEXT_COLOR)
        self.screen.blit(label, label.get_rect(center=rect.center))

    def draw(self):
        self.screen.fill(MENU_BG_COLOR)

        # TITLE
        self.title_width_pos = self.screen.get_width() // 2
        self.title_height_pos = self.screen.get_height() // 2 - MENU_TITLE_Y_OFFSET

        font_title = pygame.font.SysFont(None, MENU_TITLE_FONT_SIZE)

        title = font_title.render("CakeCraft", True, MENU_TITLE_COLOR)

        self.screen.blit(title, title.get_rect(center=(self.title_width_pos, self.title_height_pos)))

        # BUTTONS
        btn_x = self.screen.get_width() // 2 - MENU_BTN_WIDTH // 2
        self.draw_button(MenuButton.JOUER, btn_x, 400, MENU_BTN_WIDTH, MENU_BTN_HEIGHT)
        self.draw_button(MenuButton.SCORE, btn_x, 540, MENU_BTN_WIDTH, MENU_BTN_HEIGHT)
        self.draw_button(MenuButton.QUITTER, btn_x, 680, MENU_BTN_WIDTH, MENU_BTN_HEIGHT)

        pygame.display.flip()

    def run(self) -> MenuButton | None:
        while self.running:
            self.handle_events()
            self.draw()
        return self.next_screen


if __name__ == "__main__":
    pygame.init()
    menu = Menu()
    menu.run()
    pygame.quit()
