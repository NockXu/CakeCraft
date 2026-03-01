from core.position import Position
import pygame

class Interactable:
    def __init__(self, position: Position, collision_size: int = 50,
                 text: str = "à remplacer", activate_keys=None):
        self.position       = position
        self.collision_size = collision_size
        self.in_range       = False
        self.text           = text
        self.activate_keys  = activate_keys

    def get_collision_rect(self):
        half = self.collision_size // 2
        return pygame.Rect(
            self.position.x - half,
            self.position.y - half,
            self.collision_size,
            self.collision_size,
        )

    def draw_collision_zone(self, screen: pygame.Surface, color: tuple = (0, 255, 0), alpha: int = 50):
        surf = pygame.Surface((self.collision_size, self.collision_size))
        surf.set_alpha(alpha)
        surf.fill(color)
        screen.blit(surf, (self.position.x - self.collision_size // 2,
                           self.position.y - self.collision_size // 2))

    def draw_help(self, screen: pygame.Surface, color: tuple = (0, 0, 0)):
        if self.in_range:
            font = pygame.font.Font(None, 20)
            surf = font.render(self.text, True, color)
            screen.blit(surf, (self.position.x, self.position.y))
