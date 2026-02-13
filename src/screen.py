import pygame

class Screen:
    def __init__(self):
        self.width = 1280
        self.height = 1024
        self.icon = pygame.image.load('./assets/icon/icon.png')
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN | pygame.SCALED)
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("CakeCraft")

if __name__ == "__main__":
    pygame.init()
    
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