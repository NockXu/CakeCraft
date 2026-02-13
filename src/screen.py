from constants import SCREEN_HEIGHT, SCREEN_WIDTH, ICON_PATH
import pygame

class Screen:
    def __init__(self):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.icon = pygame.image.load(ICON_PATH)
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN | pygame.SCALED)
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("CakeCraft")

if __name__ == "__main__":
    pygame.init()
    screen = Screen()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.screen.fill((255, 255, 255))
        pygame.display.flip()
    
    pygame.quit()