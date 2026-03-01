import pygame
from entity.item.item import Item
from core.position import Position
from core.enums import Ingredient

# (background, text) colors per ingredient
_COLORS = {
    Ingredient.FLOUR:      ((248, 242, 228), (112, 86,  52)),
    Ingredient.EGG:        ((255, 222, 85),  (112, 78,  0)),
    Ingredient.BUTTER:     ((255, 200, 8),   (112, 78,  0)),
    Ingredient.SUGAR:      ((255, 182, 202), (152, 48,  85)),
    Ingredient.CREAM:      ((244, 226, 212), (105, 76,  50)),
    Ingredient.CHOCOLATE:  ((88,  42,  12),  (255, 225, 192)),
    Ingredient.STRAWBERRY: ((222, 56,  76),  (255, 236, 240)),
    Ingredient.VANILLA:    ((198, 178, 228), (78,  50,  110)),
}

_font = None

class IngredientItem(Item):
    def __init__(self, position: Position, ingredient_type: Ingredient):
        bg, _ = _COLORS.get(ingredient_type, ((200, 200, 200), (0, 0, 0)))
        super().__init__(position, name=ingredient_type.value, size=30, color=bg)
        self.ingredient_type = ingredient_type

    def _render(self, screen: pygame.Surface, cx: int, cy: int):
        global _font
        if _font is None:
            _font = pygame.font.Font(None, 16)

        bg, fg = _COLORS.get(self.ingredient_type, ((200, 200, 200), (0, 0, 0)))
        rect = pygame.Rect(cx - self.size // 2, cy - self.size // 2, self.size, self.size)
        pygame.draw.rect(screen, bg, rect, border_radius=6)
        pygame.draw.rect(screen, fg, rect, 2, border_radius=6)

        # Abbreviated label (first 2 chars)
        abbr = self.ingredient_type.value[:2].upper()
        label = _font.render(abbr, True, fg)
        screen.blit(label, label.get_rect(center=(cx, cy)))
