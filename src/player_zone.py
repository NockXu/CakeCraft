import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from enums import Side, CustomerState
from constants import (
    MAP_SEPARATOR_COLOR, MAP_SEPARATOR_WIDTH, MAP_KITCHEN_RATIO,
    MAP_INGREDIENT_BOX_RATIO, MAP_CUSTOMER_GAP_RATIO,
    MAP_COMPTOIR_HEIGHT, MAP_COMPTOIR_COLOR,
    PLAYER_SIZE, PLAYER_1_COLOR, PLAYER_2_COLOR,
    CUSTOMER_SIZE, CUSTOMER_SPAWN_INTERVAL, CUSTOMER_MAX_COUNT,
    PLAYER_1_KEYS, PLAYER_2_KEYS
)
from entity.player import Player
from entity.customer import Customer
from position import Position
from recipe_catalog import RecipeCatalog


_ORDER_FONT_TITLE = None
_ORDER_FONT_ITEM  = None
_ORDER_PADDING    = 12


class PlayerZone:
    def __init__(self, screen: pygame.Surface, side: Side):
        self.screen = screen
        self.side   = side

        w      = screen.get_width()
        h      = screen.get_height()
        half_w = w // 2

        x_offset = 0 if side == Side.LEFT else half_w

        # Kitchen (top portion)
        kitchen_h = int(h * MAP_KITCHEN_RATIO)
        self.kitchen_rect = pygame.Rect(x_offset, 0, half_w, kitchen_h)

        # Shop area (bottom portion)
        shop_h = h - kitchen_h
        shop_y = kitchen_h

        # Gap — vertical customer path height
        gap_h         = int(shop_h * MAP_CUSTOMER_GAP_RATIO)
        self._gap_top = shop_y
        self._gap_bot = shop_y + gap_h

        # Ingredient / order box
        box_w = int(half_w * MAP_INGREDIENT_BOX_RATIO)
        box_x = x_offset if side == Side.LEFT else x_offset + half_w - box_w
        box_y = self._gap_bot
        box_h = shop_h - gap_h
        self.ingredient_box_rect = pygame.Rect(box_x, box_y, box_w, box_h)

        # Path — the vertical corridor customers walk through
        # For LEFT: path is to the RIGHT of the ingredient box
        # For RIGHT: path is to the LEFT of the ingredient box
        path_w = half_w - box_w
        if side == Side.LEFT:
            controls = PLAYER_1_KEYS
            path_x = x_offset + box_w
        else:
            controls = PLAYER_2_KEYS
            path_x = x_offset
        self._path_cx = path_x + path_w // 2

        # Comptoir — drawn at the top of the path, same width as path
        self.comptoir_rect = pygame.Rect(path_x, self._gap_top, path_w, MAP_COMPTOIR_HEIGHT)

        # Customer positions
        # Spawn  — at path center, just below the gap (bottom of screen area)
        # Wait   — at path center, just below the comptoir
        # Leave  — horizontally off-screen in their direction
        _leave_x = -CUSTOMER_SIZE if side == Side.LEFT else w + CUSTOMER_SIZE
        self._spawn_pos = Position(self._path_cx, h - CUSTOMER_SIZE)
        self._wait_pos  = Position(self._path_cx, self._gap_top + MAP_COMPTOIR_HEIGHT + CUSTOMER_SIZE + 4)
        self._leave_pos = Position(_leave_x,      self._gap_top + MAP_COMPTOIR_HEIGHT + CUSTOMER_SIZE + 4)

        # Player
        color = PLAYER_1_COLOR if side == Side.LEFT else PLAYER_2_COLOR
        self.player = Player(
            Position(self.kitchen_rect.centerx, self.kitchen_rect.centery),
            PLAYER_SIZE, color, self.kitchen_rect, controls
        )

        # Customer management
        self._customers:   list[Customer] = []
        self._spawn_timer: float          = CUSTOMER_SPAWN_INTERVAL

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update(self, dt: float):
        self._spawn_timer -= dt
        if self._spawn_timer <= 0 and len(self._customers) < CUSTOMER_MAX_COUNT:
            self._spawn_customer()
            self._spawn_timer = CUSTOMER_SPAWN_INTERVAL

        self._update_queue_positions()

        for customer in self._customers:
            customer.update(dt)
        self._customers = [c for c in self._customers if not c.is_done]

    def _update_queue_positions(self):
        """Recalculate each customer's wait position so they queue up without overlapping.
        Only the customer at index 0 (front) gets promoted to WAITING and starts their timer."""
        spacing = CUSTOMER_SIZE * 2 + 4

        # Include WALKING, QUEUED and WAITING — all occupy a spot in line
        in_line = [c for c in self._customers
                   if c.state in (CustomerState.WALKING, CustomerState.QUEUED, CustomerState.WAITING)]

        # Sort by y ascending — smallest y = closest to the comptoir (front of queue)
        in_line.sort(key=lambda c: c.position.y)

        for i, customer in enumerate(in_line):
            if i == 0:
                # Front of queue — assign the comptoir wait position
                customer.wait_position = Position(self._wait_pos.x, self._wait_pos.y)
                # Promote to WAITING (start timer) once they've physically arrived
                if customer.state == CustomerState.QUEUED and customer._reached(customer.wait_position):
                    customer.state = CustomerState.WAITING
            else:
                # Spot is directly behind the customer ahead (based on their assigned wait_position)
                prev_y = in_line[i - 1].wait_position.y
                customer.wait_position = Position(self._wait_pos.x, prev_y + spacing)
                # Safety: demote back to QUEUED if somehow not at front
                if customer.state == CustomerState.WAITING:
                    customer.state = CustomerState.QUEUED

    def _spawn_customer(self):
        recipe   = RecipeCatalog.random()
        customer = Customer(
            position       = Position(self._spawn_pos.x, self._spawn_pos.y),
            wait_position  = Position(self._wait_pos.x,  self._wait_pos.y),
            leave_position = Position(self._leave_pos.x, self._leave_pos.y),
            recipe         = recipe,
        )
        self._customers.append(customer)

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------

    def draw(self):
        # Ingredient / order box border
        pygame.draw.rect(self.screen, MAP_SEPARATOR_COLOR, self.ingredient_box_rect, MAP_SEPARATOR_WIDTH)

        # Comptoir — at the top of the path, same width as the path
        pygame.draw.rect(self.screen, MAP_COMPTOIR_COLOR, self.comptoir_rect)

        # Order panel
        waiting = next((c for c in self._customers if c.is_waiting), None)
        self._draw_order_panel(waiting)

        # Customers and player
        for customer in self._customers:
            customer.draw(self.screen)
        self.player.draw(self.screen)

    def _draw_order_panel(self, customer: Customer | None):
        global _ORDER_FONT_TITLE, _ORDER_FONT_ITEM
        if _ORDER_FONT_TITLE is None:
            _ORDER_FONT_TITLE = pygame.font.SysFont(None, 28)
            _ORDER_FONT_ITEM  = pygame.font.SysFont(None, 22)

        box = self.ingredient_box_rect
        pad = _ORDER_PADDING

        if customer is None:
            label = _ORDER_FONT_ITEM.render("Pas de commande", True, (160, 160, 160))
            self.screen.blit(label, label.get_rect(center=box.center))
            return

        recipe = customer.recipe
        y      = box.top + pad

        # Recipe title
        title = _ORDER_FONT_TITLE.render(recipe.cake_type.value, True, (50, 50, 50))
        self.screen.blit(title, (box.left + pad, y))
        y += title.get_height() + 6

        # Divider line
        pygame.draw.line(self.screen, MAP_SEPARATOR_COLOR,
                         (box.left + pad, y), (box.right - pad, y), 1)
        y += 8

        # Ingredients list
        for ingredient in recipe.ingredients:
            item = _ORDER_FONT_ITEM.render(f"• {ingredient.value}", True, (80, 80, 80))
            self.screen.blit(item, (box.left + pad, y))
            y += item.get_height() + 4

        # Patience bar at the very bottom of the box
        ratio     = customer.patience_ratio
        bar_color = (int(255 * (1 - ratio)), int(200 * ratio), 0)
        bar_rect  = pygame.Rect(box.left, box.bottom - MAP_SEPARATOR_WIDTH,
                                box.width, MAP_SEPARATOR_WIDTH)
        pygame.draw.rect(self.screen, (200, 200, 200), bar_rect)
        pygame.draw.rect(self.screen, bar_color,
                         pygame.Rect(bar_rect.left, bar_rect.top,
                                     int(bar_rect.width * ratio), bar_rect.height))
