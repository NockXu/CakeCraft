import pygame
import math
from interactable.interactable import Interactable
from entity.item.cake_item import CakeItem
from core.position import Position
from core.enums import DeliveryResult

_font = None


class Counter(Interactable):
    """Comptoir de livraison — le joueur dépose le gâteau ici pour servir le client."""

    def __init__(self, position: Position, collision_size: int, player,
                 activate_key: int = pygame.K_f):
        super().__init__(position, collision_size=collision_size,
                         text="Livrer la commande (F)", activate_keys=activate_key)
        self.player       = player
        self.activate_key = activate_key
        self.on_delivery  = None    # callback(result) set by PlayerZone

        self._flash_timer   = 0.0
        self._flash_success = True
        self._quality_multiplier = 1.0  # Stocke le multiplicateur de qualité

    def _calculate_cooking_quality(self, cooked_level: float) -> float:
        """
        Calcule le multiplicateur de qualité basé sur la cuisson:
        - 0.0 à 0.9: plus c'est cuit, plus de points (progression linéaire)
        - 0.91 à 1.11: score maximum (100% des points)
        - 1.12 à 2.0: moins de points (dégradation linéaire)
        Retourne un float entre 0 et 1
        """
        if cooked_level <= 0.9:
            # Progression linéaire de 0.1 à 1.0
            # 0.0 -> 0.1x, 0.9 -> 1.0x
            return 0.1 + (cooked_level / 0.9) * 0.9
        elif cooked_level <= 1.11:
            # Zone parfaite : score maximum
            return 1.0
        else:
            # Dégradation de 1.0 à 0.1
            # 1.12 -> 0.98x, 2.0 -> 0.1x
            t = (cooked_level - 1.11) / (2.0 - 1.11)  # 0 à 1
            return 1.0 - t * 0.9  # 1.0 -> 0.1

    def get_quality_multiplier(self) -> float:
        """Retourne le multiplicateur de qualité actuel, arrondi au supérieur"""
        return math.ceil(self._quality_multiplier * 10) / 10  # Arrondi à 0.1 près

    def update(self, dt: float):
        self._flash_timer = max(0.0, self._flash_timer - dt)

    def handle_keydown(self, key):
        if key != self.activate_key or not self.in_range:
            return

        result = self._try_deliver()
        self._flash_timer   = 0.6
        self._flash_success = (result == DeliveryResult.SUCCESS)

        if self.on_delivery:
            self.on_delivery(result)

    def _try_deliver(self) -> DeliveryResult:
        if not self.player.has_item():
            return DeliveryResult.WRONG_ITEM
        if not isinstance(self.player.current_item, CakeItem):
            return DeliveryResult.WRONG_ITEM
        if not self.player.current_item.cooked > 0:
            return DeliveryResult.NOT_COOKED
        
        # Calculer la qualité de cuisson
        cake = self.player.current_item
        self._quality_multiplier = self._calculate_cooking_quality(cake.cooked)
        
        return DeliveryResult.SUCCESS   # zone handles actual serving via callback

    def handle_movement(self):
        pass

    def draw(self, screen: pygame.Surface):
        global _font
        if _font is None:
            _font = pygame.font.Font(None, 18)

        rect = self.get_collision_rect()

        # Flash on delivery attempt
        if self._flash_timer > 0:
            color = (80, 200, 80) if self._flash_success else (200, 60, 60)
        else:
            color = (210, 170, 90)

        pygame.draw.rect(screen, color, rect, border_radius=6)
        pygame.draw.rect(screen, (100, 70, 20), rect, 2, border_radius=6)

        label = _font.render("Livraison", True, (40, 20, 0))
        screen.blit(label, label.get_rect(center=rect.center))
        self.draw_help(screen)
