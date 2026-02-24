import sys
import os
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
    
    def pick_up_cake(self, cake):
        """Le joueur prend un gâteau"""
        if cake not in self.children:
            self.add_child(cake)
            cake.carried_by = self
            return True
        return False
    
    def drop_cake(self, cake):
        """Le joueur lâche un gâteau"""
        if cake in self.children:
            self.remove_child(cake)
            cake.carried_by = None
            return True
        return False
    
    def drop_all_cakes(self):
        """Le joueur lâche tous les gâteaux"""
        for child in self.children[:]:
            self.drop_cake(child)
    
    def get_carried_cakes(self):
        """Retourne la liste des gâteaux portés"""
        return self.children.copy()
    
    def handle_events(self, keys):
        """Gère les événements de mouvement selon le joueur"""
        if keys[self.controls["left"]]:
            self.move(-PLAYER_SPEED, 0)
        if keys[self.controls["right"]]:
            self.move(PLAYER_SPEED, 0)
        if keys[self.controls["up"]]:
            self.move(0, -PLAYER_SPEED)
        if keys[self.controls["down"]]:
            self.move(0, PLAYER_SPEED)
