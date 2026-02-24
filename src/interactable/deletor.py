import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from entity.item.item import Item
from interactable.interactable import Interactable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from position import Position
import pygame
from entity.player import Player

class Deletor(Interactable):
    def __init__(self, position: Position, collision_size: int, text: str, activate_key: int = None, player: Player = None):
        super().__init__(position, collision_size=collision_size, text=text, activate_keys=activate_key)
        self.player = player
        self.activate_key = activate_key

    def delete_item(self) -> bool:
        """Supprime l'item du joueur"""
        if self.in_range and self.player.has_item():
            self.player.remove_item()
            return True
        return False

    def draw(self, screen: pygame.Surface):
        self.draw_collision_zone(screen)
        self.draw_help(screen)

    def handle_keydown(self, key):
        """Gère les événements de touche pressée"""
        if key == self.activate_key:
            self.delete_item()

    def handle_movement(self):
        pass