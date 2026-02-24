import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from position import Position
import pygame

class Interactable:
    def __init__(self, position: Position, collision_size: int = 50, text: str = "à remplacer", activate_keys: list = []):
        self.position = position
        self.collision_size = collision_size
        self.in_range : bool = False
        self.text : str = text
        self.activate_keys = activate_keys
    
    def get_collision_rect(self):
        """Retourne le rectangle de collision centré sur la position"""
        half_size = self.collision_size // 2
        return pygame.Rect(
            self.position.x - half_size,
            self.position.y - half_size,
            self.collision_size,
            self.collision_size
        )
    
    def draw_collision_zone(self, screen: pygame.Surface, color: tuple = (0, 255, 0), alpha: int = 50):
        """Dessine la zone de collision (pour debug)"""
        collision_surface = pygame.Surface((self.collision_size, self.collision_size))
        collision_surface.set_alpha(alpha)
        collision_surface.fill(color)
        screen.blit(collision_surface, 
                   (self.position.x - self.collision_size//2, 
                    self.position.y - self.collision_size//2))

    def draw_help(self, screen: pygame.Surface, color: tuple = (0, 0, 0)):
        if self.in_range:
            font = pygame.font.Font(None, 20)
            text_surface = font.render(self.text, True, color)
            screen.blit(text_surface, (self.position.x, self.position.y))