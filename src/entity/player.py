import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from entity.entity import Entity
from position import Position
import pygame


class Player(Entity):
    def __init__(self, position: Position, size: int = 20, color: tuple = (255, 0, 0), boundary: pygame.Rect = None):
        super().__init__(position)
        self.size = size
        self.color = color
        self.boundary = boundary

    def move(self, dx: int, dy: int):
        super().move(dx, dy)
        if self.boundary:
            half = self.size // 2
            self.position.x = max(self.boundary.left + half, min(self.position.x, self.boundary.right - half))
            self.position.y = max(self.boundary.top + half, min(self.position.y, self.boundary.bottom - half))

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color,
                        (self.position.x - self.size // 2,
                         self.position.y - self.size // 2,
                         self.size, self.size))

        for child in self.children:
            child.draw(screen)
