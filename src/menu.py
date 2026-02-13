import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from screen import Screen

class Menu:
    def __init__(self):
        self.screen: pygame.Surface = Screen().screen
        self.running = True
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
                        print(f"Button clicked: {spec}")

    def draw_button(self, spec: str, x: int, y: int, width: int, height: int):
        rect = pygame.Rect(x, y, width, height)
        self.buttons[spec] = rect
        pygame.draw.rect(self.screen, (255, 255, 0), rect, border_radius=32)
        font = pygame.font.SysFont(None, 64)
        label = font.render(spec, True, (0, 0, 0))
        self.screen.blit(label, label.get_rect(center=rect.center))

    def draw(self):
        self.screen.fill((140, 0, 90)) # color

        # TITLE
        self.title_width_pos = self.screen.get_width() // 2
        self.title_height_pos = self.screen.get_height() // 2 - 300 # 300 is to raise the height

        font_title = pygame.font.SysFont(None, 160)

        title = font_title.render("CakeCraft", True, (255, 255, 255))

        self.screen.blit(title, title.get_rect(center=(self.title_width_pos, self.title_height_pos)))

        # BUTTONS
        btn_width = 400
        btn_height = 120
        btn_x = self.screen.get_width() // 2 - btn_width // 2
        self.draw_button("Jouer", btn_x, 400, btn_width, btn_height)
        self.draw_button("Score", btn_x, 540, btn_width, btn_height)
        self.draw_button("Quitter", btn_x, 680, btn_width, btn_height)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()


if __name__ == "__main__":
    pygame.init()
    menu = Menu()
    menu.run()
    pygame.quit()
