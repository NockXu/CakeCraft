import pygame
import random
import os
from entity.item.item import Item
from core.position import Position
from core.enums import CakeType
from core.constants import _asset

_COLORS = {
    CakeType.VANILLA_CAKE:     ((230, 168, 10),  (85,  58,  0)),
    CakeType.CHOCOLATE_CAKE:   ((88,  42,  12),  (255, 228, 200)),
    CakeType.STRAWBERRY_CAKE:  ((202, 38,  85),  (255, 238, 244)),
    CakeType.CREAM_PUFF:       ((210, 175, 125), (72,  46,  16)),
    CakeType.CHEWING_GUM_CAKE: ((220, 80,  180), (255, 220, 240)),
    CakeType.BUTTER_BOMB:      ((255, 210, 0),   (120, 80,  0)),
    CakeType.EGG_SURPRISE:     ((255, 240, 100), (140, 100, 0)),
    CakeType.RAINBOW_MESS:     ((180, 80,  220), (255, 255, 180)),
    CakeType.CURSED_TART:      ((40,  20,  60),  (180, 100, 255)),
    CakeType.CLOUD_CAKE:       ((220, 235, 255), (80,  100, 160)),
}

_cake_sprite_paths: list[str] = []
_cake_sprite_paths_loaded = False
_sprite_cache: dict[tuple, pygame.Surface] = {}


def _ensure_paths_loaded():
    global _cake_sprite_paths, _cake_sprite_paths_loaded
    if _cake_sprite_paths_loaded:
        return
    _cake_sprite_paths_loaded = True
    cakes_dir = _asset('sprites', 'cakes')
    try:
        for fname in os.listdir(cakes_dir):
            if fname.lower().endswith('.png'):
                _cake_sprite_paths.append(os.path.join(cakes_dir, fname))
    except Exception:
        pass


def _get_sprite(path: str, size: int) -> pygame.Surface | None:
    key = (path, size)
    if key not in _sprite_cache:
        try:
            surf = pygame.image.load(path).convert_alpha()
            surf = pygame.transform.smoothscale(surf, (size, size))
        except Exception:
            surf = None
        _sprite_cache[key] = surf
    return _sprite_cache[key]


def _tint(surf: pygame.Surface, r: int, g: int, b: int) -> pygame.Surface:
    tinted = surf.copy()
    tinted.fill((r, g, b, 255), special_flags=pygame.BLEND_RGBA_MULT)
    return tinted

def _make_white(surf: pygame.Surface) -> pygame.Surface:
    """Force all RGB to 255, keep original alpha channel."""
    white = surf.copy()
    white.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_MAX)
    return white


class CakeItem(Item):

    cooked: float = 0.0

    def __init__(self, position: Position, cake_type: CakeType):
        bg, _ = _COLORS.get(cake_type, ((200, 200, 200), (0, 0, 0)))
        super().__init__(position, name=cake_type.value, size=34, color=bg)
        self.cake_type = cake_type
        _ensure_paths_loaded()
        self._sprite_path = random.choice(_cake_sprite_paths) if _cake_sprite_paths else None

    def _render(self, screen: pygame.Surface, cx: int, cy: int):
        """Render with cooking state: white→color (0→1), color→black (1→2)."""
        self._draw_cooked(screen, cx, cy, self.size)

    def render_in_oven(self, screen: pygame.Surface, cx: int, cy: int, size: int):
        """Same effect but at a custom size, used for the in-oven display."""
        self._draw_cooked(screen, cx, cy, size)

    def _draw_cooked(self, screen: pygame.Surface, cx: int, cy: int, size: int):
        sprite = _get_sprite(self._sprite_path, size) if self._sprite_path else None
        c = self.cooked

        if sprite:
            if c <= 0.0:
                drawn = _make_white(sprite)
            elif c < 1.0:
                # white → full color
                white = _make_white(sprite)
                colored = sprite.copy()
                colored.set_alpha(int(c * 255))
                white.blit(colored, (0, 0))
                drawn = white
            elif c <= 1.0:
                drawn = sprite.copy()
            else:
                # full color → black
                t = min(1.0, c - 1.0)
                v = int((1.0 - t) * 255)
                drawn = _tint(sprite, v, v, v)
            screen.blit(drawn, drawn.get_rect(center=(cx, cy)))
        else:
            bg, fg = _COLORS.get(self.cake_type, ((200, 200, 200), (0, 0, 0)))
            if c <= 1.0:
                t = max(0.0, c)
                r = int(255 + (bg[0] - 255) * t)
                g = int(255 + (bg[1] - 255) * t)
                b = int(255 + (bg[2] - 255) * t)
            else:
                t = min(1.0, c - 1.0)
                r = int(bg[0] * (1.0 - t))
                g = int(bg[1] * (1.0 - t))
                b = int(bg[2] * (1.0 - t))
            rect = pygame.Rect(cx - size // 2, cy - size // 2, size, size)
            pygame.draw.rect(screen, (r, g, b), rect, border_radius=8)
            pygame.draw.rect(screen, fg, rect, 2, border_radius=8)
