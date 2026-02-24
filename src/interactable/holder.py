import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from entity.item.item import Item
from interactable.interactable import Interactable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from position import Position
import pygame
from entity.player import Player
import copy

class Holder(Interactable):
    def __init__(self, position: Position, collision_size: int, text: str, activate_key: int = None, player: Player = None):
        super().__init__(position, collision_size=collision_size, text=text, activate_keys=activate_key)
        self.player = player
        self.activate_key = activate_key
        self.held_item = None

    def hold_item(self) -> bool:
        """Prend l'item du joueur et le garde"""
        if self.in_range and self.player.has_item():
            self.held_item = self.player.remove_item()
            self.held_item.position = self.position
            return True
        return False

    def retrieve_item(self) -> bool:
        """Retourne l'item au joueur"""
        if self.in_range and self.held_item and not self.player.has_item():
            self.player.give_item(self.held_item)
            self.held_item.position = self.player.position
            self.held_item = None
            return True
        return False

    def draw(self, screen: pygame.Surface):
        self.draw_collision_zone(screen)
        self.draw_help(screen)
        # Dessiner l'item tenu si présent
        if self.held_item:
            self.held_item.draw(screen)

    def handle_keydown(self, key):
        """Gère les événements de touche pressée"""
        if key == self.activate_key:
            if self.held_item:
                self.retrieve_item()
            else:
                self.hold_item()

    def handle_movement(self):
        pass