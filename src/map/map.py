import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from screen import Screen

class Map:
    def __init__(self):
        self.screen: pygame.Surface = Screen().screen
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def draw(self):
        self.screen.fill((255, 255, 255))

        # SEPARATOR
        center_x = self.screen.get_width() // 2
        pygame.draw.line(self.screen, (0, 0, 0), (center_x, 0), (center_x, self.screen.get_height()), 4)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
