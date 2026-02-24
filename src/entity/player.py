import sys
import os

from interactable.interactable import Interactable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from entity.entity import Entity
from position import Position
import pygame
from constants import PLAYER_SPEED, PLAYER_1_KEYS, PLAYER_2_KEYS


class Player(Entity):
    def __init__(self, position: Position, size: int = 20, color: tuple = (255, 0, 0), boundary: pygame.Rect = None, controls: dict = None):
        super().__init__(position)
        self.size = size
        self.color = color
        self.boundary = boundary
        self.controls = controls
        self.collision_size = size + 10  # Zone de collision plus grande que le joueur
        self.available_interactables : list[Interactable] = []
        self.current_item = None  # Item actuellement porté par le joueur

    def move(self, dx: int, dy: int):
        if self.boundary:
            # Calculer la nouvelle position avant de bouger
            new_x = self.position.x + dx
            new_y = self.position.y + dy
            
            # Appliquer les limites
            half = self.size // 2
            new_x = max(self.boundary.left + half, min(new_x, self.boundary.right - half))
            new_y = max(self.boundary.top + half, min(new_y, self.boundary.bottom - half))
            
            # Calculer le mouvement final et l'appliquer
            final_dx = new_x - self.position.x
            final_dy = new_y - self.position.y
            
            if final_dx != 0 or final_dy != 0:
                super().move(final_dx, final_dy)
        else:
            # Pas de limite, mouvement normal
            super().move(dx, dy)

    def draw(self, screen: pygame.Surface):
        # Dessiner la zone de collision (transparente bleue)
        collision_surface = pygame.Surface((self.collision_size, self.collision_size))
        collision_surface.set_alpha(30)
        collision_surface.fill((0, 100, 255))
        screen.blit(collision_surface, 
                   (self.position.x - self.collision_size//2, 
                    self.position.y - self.collision_size//2))
        
        # Dessiner le joueur
        pygame.draw.rect(screen, self.color,
                        (self.position.x - self.size // 2,
                         self.position.y - self.size // 2,
                         self.size, self.size))

        for child in self.children:
            child.draw(screen)
    
    def handle_events(self):
        """Gère les événements du joueur"""

        interactable_in_range = self.check_collision_with_interactables()

        for interactable in self.available_interactables:
            if interactable == interactable_in_range:
                interactable.in_range = True
            else:
                interactable.in_range = False

    def handle_movement(self, keys):
        """Gère les mouvements du joueur"""
        if keys[self.controls["left"]]:
            self.move(-PLAYER_SPEED, 0)
        if keys[self.controls["right"]]:
            self.move(PLAYER_SPEED, 0)
        if keys[self.controls["up"]]:
            self.move(0, -PLAYER_SPEED)
        if keys[self.controls["down"]]:
            self.move(0, PLAYER_SPEED)
    
    def get_collision_rect(self):
        """Retourne le rectangle de collision du joueur"""
        half_size = self.collision_size // 2
        return pygame.Rect(
            self.position.x - half_size,
            self.position.y - half_size,
            self.collision_size,
            self.collision_size
        )
    
    def check_collision_with_interactables(self) -> Interactable | None:
        """Vérifie si la zone de collision du joueur intersecte avec un objet Interactable"""
        player_rect = self.get_collision_rect()
        for interactable in self.available_interactables:
            interactable_rect = interactable.get_collision_rect()
            if player_rect.colliderect(interactable_rect):
                return interactable
        return None

    def give_item(self, item):
        """Donne un item au joueur (l'ajoute à ses enfants)"""
        if item and self.current_item is None:
            self.current_item = item
            self.add_child(item)
            return True
        return False

    def remove_item(self):
        """Retire l'item actuel du joueur et le retourne"""
        if self.current_item:
            item = self.current_item
            self.current_item = None
            self.remove_child(item)
            return item
        return None

    def has_item(self):
        """Retourne True si le joueur porte un item"""
        return self.current_item is not None
