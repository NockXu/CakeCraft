import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from entity.entity import Entity
from position import Position
import pygame

class Item(Entity):
    def __init__(self, position: Position, name: str, size: int = 20, color: tuple = (255, 0, 0)):
        super().__init__(position)
        self.size = size
        self.color = color
        self.name = name
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, 
                        (self.position.x - self.size//2, 
                         self.position.y - self.size//2, 
                         self.size, self.size))