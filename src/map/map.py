import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from screen import Screen

class Map:
    def __init__(self):
        self.screen : pygame.Surface = screen.Screen().screen

if __name__ == "__main__":
    pygame.init()
    map = Map()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        map.screen.fill((255, 255, 255))
        pygame.display.flip()
    
    pygame.quit()
