import pygame
from interactable.interactable import Interactable
from entity.item.ingredient_item import IngredientItem, _COLORS as _ING_COLORS
from entity.item.cake_item import CakeItem
from core.position import Position
from core.enums import Ingredient

_font_label = None
_font_small = None


class Workbench(Interactable):
    """Plan de travail — le joueur y dépose ses ingrédients un par un.
    Quand la recette est complète, un CakeItem est créé et peut être récupéré."""

    def __init__(self, position: Position, collision_size: int, player,
                 activate_key: int = pygame.K_f):
        super().__init__(position, collision_size=collision_size,
                         text="Déposer / Récupérer (F)", activate_keys=activate_key)
        self.player          = player
        self.activate_key    = activate_key
        self.current_recipe  = None     # set by PlayerZone each frame
        self._deposited      = []       # list of Ingredient deposited so far
        self._output_item    = None     # CakeItem ready to pick up

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def reset(self):
        """Vider le plan de travail (nouveau client ou mauvaise livraison)."""
        self._deposited   = []
        self._output_item = None

    def get_deposited(self) -> list:
        return list(self._deposited)

    # ------------------------------------------------------------------
    # Interaction
    # ------------------------------------------------------------------

    def handle_keydown(self, key):
        if key != self.activate_key or not self.in_range:
            return

        # Priority 1: player picks up finished cake
        if self._output_item is not None and not self.player.has_item():
            self.player.give_item(self._output_item)
            self._output_item = None
            return

        # Priority 2: player deposits an ingredient
        if self.player.has_item() and isinstance(self.player.current_item, IngredientItem):
            ingr = self.player.current_item.ingredient_type
            self.player.remove_item()
            self._deposited.append(ingr)
            # Check if the recipe is complete
            if self.current_recipe and self._is_complete():
                self._assemble_cake()

    def _is_complete(self) -> bool:
        needed = sorted(i.name for i in self.current_recipe.ingredients)
        have   = sorted(i.name for i in self._deposited)
        return have == needed

    def _assemble_cake(self):
        self._output_item = CakeItem(
            Position(self.position.x, self.position.y),
            self.current_recipe.cake_type,
        )
        self._deposited = []

    def handle_movement(self):
        pass

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------

    def draw(self, screen: pygame.Surface):
        global _font_label, _font_small
        if _font_label is None:
            _font_label = pygame.font.Font(None, 18)
            _font_small = pygame.font.Font(None, 14)

        rect = self.get_collision_rect()

        # Background
        bg_color = (140, 85, 30) if self._output_item else (180, 120, 60)
        pygame.draw.rect(screen, bg_color, rect, border_radius=8)
        pygame.draw.rect(screen, (80, 45, 10), rect, 2, border_radius=8)

        # Title
        title = _font_label.render("Plan de travail", True, (255, 235, 200))
        screen.blit(title, title.get_rect(centerx=rect.centerx, top=rect.top + 4))

        # Deposited ingredients as small colored dots
        dot_r = 5
        dot_y = rect.top + 22
        dot_x = rect.left + 8
        for ingr in self._deposited:
            bg, _ = _ING_COLORS.get(ingr, ((200, 200, 200), (0, 0, 0)))
            pygame.draw.circle(screen, bg, (dot_x + dot_r, dot_y + dot_r), dot_r)
            pygame.draw.circle(screen, (60, 30, 0), (dot_x + dot_r, dot_y + dot_r), dot_r, 1)
            dot_x += dot_r * 2 + 4
            if dot_x + dot_r * 2 > rect.right - 4:
                dot_x  = rect.left + 8
                dot_y += dot_r * 2 + 4

        # Output cake ready indicator
        if self._output_item:
            ready_label = _font_label.render("Gâteau prêt !", True, (255, 255, 100))
            screen.blit(ready_label, ready_label.get_rect(centerx=rect.centerx, bottom=rect.bottom - 4))
            self._output_item._render(screen, rect.centerx, rect.centery + 8)

        self.draw_help(screen)
