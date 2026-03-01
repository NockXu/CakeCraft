from core.position import Position
import pygame
from hud.bubble import TextBubble

class Interactable:
    def __init__(self, position: Position, collision_size: int = 50,
                 text: str = "à remplacer", activate_keys=None):
        self.position       = position
        self.collision_size = collision_size
        self.in_range       = False
        self.text           = text
        self.activate_keys  = activate_keys
        self.help_bubble = None  # Bulle d'aide initialisée à la demande

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
            # Initialiser la bulle d'aide si nécessaire
            if self.help_bubble is None:
                # Calculer la taille de la bulle en fonction du texte
                font = pygame.font.Font(None, 16)
                text_surf = font.render(self.text, True, color)
                bubble_width = text_surf.get_width() + 20  # Padding horizontal
                bubble_height = text_surf.get_height() + 15  # Padding vertical
                
                # Positionner la bulle au-dessus de l'interactable
                bubble_x = self.position.x - bubble_width // 2
                bubble_y = self.position.y - self.collision_size - bubble_height - 5
                
                self.help_bubble = TextBubble(bubble_x, bubble_y, bubble_width, bubble_height, padding=5)
            
            # Dessiner la bulle d'aide
            self.help_bubble.draw(screen)
            font = pygame.font.Font(None, 16)
            self.help_bubble.draw_text(screen, self.text, font, color, centered=True)
        else:
            # Réinitialiser la bulle quand on n'est plus dans la zone
            self.help_bubble = None
