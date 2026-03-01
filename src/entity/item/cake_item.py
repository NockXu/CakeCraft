import pygame
from entity.item.item import Item
from core.position import Position
from core.enums import CakeType

# (background, text) colors per cake type
_COLORS = {
    CakeType.VANILLA_CAKE:    ((230, 168, 10),  (85,  58,  0)),
    CakeType.CHOCOLATE_CAKE:  ((88,  42,  12),  (255, 228, 200)),
    CakeType.STRAWBERRY_CAKE: ((202, 38,  85),  (255, 238, 244)),
    CakeType.CREAM_PUFF:      ((210, 175, 125), (72,  46,  16)),
}

_font_big  = None
_font_small = None

class CakeItem(Item):

    cooked : float = 0.0
    
    def __init__(self, position: Position, cake_type: CakeType):
        bg, _ = _COLORS.get(cake_type, ((200, 200, 200), (0, 0, 0)))
        super().__init__(position, name=cake_type.value, size=34, color=bg)
        self.cake_type = cake_type

    def _render(self, screen: pygame.Surface, cx: int, cy: int):
        global _font_big, _font_small
        if _font_big is None:
            _font_big   = pygame.font.Font(None, 22)
            _font_small = pygame.font.Font(None, 14)

        bg, fg = _COLORS.get(self.cake_type, ((200, 200, 200), (0, 0, 0)))
        rect = pygame.Rect(cx - self.size // 2, cy - self.size // 2, self.size, self.size)
        pygame.draw.rect(screen, bg, rect, border_radius=8)
        pygame.draw.rect(screen, fg, rect, 2, border_radius=8)

        # "G" for gâteau / "C" for chou
        abbr = "C" if self.cake_type == CakeType.CREAM_PUFF else "G"
        label = _font_big.render(abbr, True, fg)
        screen.blit(label, label.get_rect(center=(cx, cy - 3)))

        # Small type indicator
        tip = _font_small.render(self.cake_type.value[:4], True, fg)
        screen.blit(tip, tip.get_rect(center=(cx, cy + 10)))