import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from entity import Entity
from position import Position
import pygame
import screen

class Player(Entity):
    def __init__(self, position: Position, size: int = 20, color: tuple = (255, 0, 0)):
        super().__init__(position)
        self.size = size
        self.color = color
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, 
                        (self.position.x - self.size//2, 
                         self.position.y - self.size//2, 
                         self.size, self.size))
        
        for child in self.children:
            child.draw(screen)

if __name__ == "__main__":
    pygame.init()
    
    screen_obj = screen.Screen()
    player = Player(Position(640, 512))
    
    clock = pygame.time.Clock()
    running = True
    speed = 5
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-speed, 0)
        if keys[pygame.K_RIGHT]:
            player.move(speed, 0)
        if keys[pygame.K_UP]:
            player.move(0, -speed)
        if keys[pygame.K_DOWN]:
            player.move(0, speed)
    
        screen_obj.screen.fill((255, 255, 255))
        player.draw(screen_obj.screen)
        pygame.display.flip()
    
        clock.tick(60)

    pygame.quit()