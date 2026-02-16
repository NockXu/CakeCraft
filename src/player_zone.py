import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from enums import Side
from constants import MAP_SEPARATOR_COLOR, MAP_SEPARATOR_WIDTH, MAP_KITCHEN_RATIO, MAP_INGREDIENT_BOX_RATIO, MAP_CUSTOMER_GAP_RATIO


class PlayerZone:
    def __init__(self, screen: pygame.Surface, side: Side):
        self.screen = screen
        self.side = side

        w = screen.get_width()
        h = screen.get_height()
        half_w = w // 2

        x_offset = 0 if side == Side.LEFT else half_w

        # Kitchen (top portion)
        kitchen_h = int(h * MAP_KITCHEN_RATIO)
        self.kitchen_rect = pygame.Rect(x_offset, 0, half_w, kitchen_h)

        # Shop area (bottom portion)
        shop_h = h - kitchen_h
        shop_y = kitchen_h

        # Gap at the top of shop area for customers to pass
        gap_h = int(shop_h * MAP_CUSTOMER_GAP_RATIO)

        # Ingredient box: bottom-RIGHT for LEFT side, bottom-LEFT for RIGHT side (near center)
        box_w = int(half_w * MAP_INGREDIENT_BOX_RATIO)
        box_x = x_offset if side == Side.LEFT else x_offset + half_w - box_w
        box_y = shop_y + gap_h
        box_h = shop_h - gap_h
        self.ingredient_box_rect = pygame.Rect(box_x, box_y, box_w, box_h)

    def draw(self):
        pygame.draw.rect(self.screen, MAP_SEPARATOR_COLOR, self.ingredient_box_rect, MAP_SEPARATOR_WIDTH)