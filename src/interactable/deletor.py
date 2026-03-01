import pygame
from interactable.interactable import Interactable
from core.position import Position

class Deletor(Interactable):
    """Poubelle — supprime l'item que le joueur porte."""

    def __init__(self, position: Position, collision_size: int, text: str,
                 activate_key: int = None, player=None):
        super().__init__(position, collision_size=collision_size,
                         text=text, activate_keys=activate_key)
        self.player       = player
        self.activate_key = activate_key

    def delete_item(self) -> bool:
        if self.in_range and self.player.has_item():
            self.player.remove_item()
            return True
        return False

    def draw(self, screen: pygame.Surface):
        rect = self.get_collision_rect()
        pygame.draw.rect(screen, (180, 60, 60), rect, border_radius=6)
        pygame.draw.rect(screen, (100, 20, 20), rect, 2, border_radius=6)

        font  = pygame.font.Font(None, 18)
        label = font.render("Poubelle", True, (255, 220, 220))
        screen.blit(label, label.get_rect(center=rect.center))
        self.draw_help(screen)

    def handle_keydown(self, key):
        if key == self.activate_key:
            self.delete_item()

    def handle_movement(self):
        pass
