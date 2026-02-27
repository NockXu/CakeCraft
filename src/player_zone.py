import pygame
import math
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from enums import Side, CustomerState, CakeType, Ingredient
from constants import (
    MAP_SEPARATOR_COLOR, MAP_SEPARATOR_WIDTH, MAP_KITCHEN_RATIO,
    MAP_INGREDIENT_BOX_RATIO, MAP_CUSTOMER_GAP_RATIO,
    MAP_COMPTOIR_HEIGHT, MAP_COMPTOIR_COLOR,
    PLAYER_SIZE, PLAYER_1_COLOR, PLAYER_2_COLOR,
    CUSTOMER_SIZE, CUSTOMER_MAX_COUNT,
    PLAYER_1_KEYS, PLAYER_2_KEYS,
    FONT_TITLE_PATH, FONT_BODY_PATH,
)
from entity.player import Player
from entity.customer import Customer
from position import Position
from interactable.creator import Creator
from interactable.deletor import Deletor
from interactable.holder import Holder
from entity.item.test import Test


# Font globals — lazily loaded on first draw
_FONT_TITLE = None   # display font for the cake name
_FONT_BODY  = None   # body font for ingredient names
_FONT_LABEL = None   # small font for section labels and timer

_PAD = 12   # general panel padding

# Cake type header palette: (background, text_color)
_CAKE_PALETTE = {
    CakeType.VANILLA_CAKE:    ((230, 168, 10),  (85, 58, 0)),
    CakeType.CHOCOLATE_CAKE:  ((88, 42, 12),    (255, 228, 200)),
    CakeType.STRAWBERRY_CAKE: ((202, 38, 85),   (255, 238, 244)),
    CakeType.CREAM_PUFF:      ((210, 175, 125), (72, 46, 16)),
}

# Ingredient badge palette: (background, text_color)
_INGREDIENT_PALETTE = {
    Ingredient.FLOUR:      ((248, 242, 228), (112, 86, 52)),
    Ingredient.EGG:        ((255, 222, 85),  (112, 78, 0)),
    Ingredient.BUTTER:     ((255, 200, 8),   (112, 78, 0)),
    Ingredient.SUGAR:      ((255, 182, 202), (152, 48, 85)),
    Ingredient.CREAM:      ((244, 226, 212), (105, 76, 50)),
    Ingredient.CHOCOLATE:  ((88, 42, 12),    (255, 225, 192)),
    Ingredient.STRAWBERRY: ((222, 56, 76),   (255, 236, 240)),
    Ingredient.VANILLA:    ((198, 178, 228), (78, 50, 110)),
}

_PANEL_BG = (252, 246, 236)   # warm cream panel background


def _draw_star(surface: pygame.Surface, cx: int, cy: int, size: int, color: tuple):
    """Draw a filled 5-pointed star centered at (cx, cy) with the given outer radius."""
    points = []
    inner = size * 0.4
    for i in range(10):
        angle = math.radians(-90 + i * 36)
        r = size if i % 2 == 0 else inner
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    pygame.draw.polygon(surface, color, points)


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
        self._customers: list[Customer] = []
        
        # Interactables management
        self.interactables = []
        self._setup_interactables()
        
        # Give interactables list to player
        self.player.available_interactables = self.interactables
    
    def _setup_interactables(self):
        """Configure les objets interactables dans la zone"""
        # Créer une machine à gâteaux dans la cuisine
        creator_x = self.kitchen_rect.centerx
        creator_y = self.kitchen_rect.centery - 50
        creator = Creator(Position(creator_x, creator_y), 50, "Machine à gâteaux", pygame.K_f, Test(), self.player)
        self.interactables.append(creator)

        # Créer un deletor (poubelle) à côté de la machine
        deletor_x = creator_x + 80
        deletor_y = creator_y
        deletor = Deletor(Position(deletor_x, deletor_y), 50, "Poubelle (supprimer)", pygame.K_f, self.player)
        self.interactables.append(deletor)

        # Créer un holder (support) en bas de la cuisine
        holder_x = self.kitchen_rect.centerx
        holder_y = self.kitchen_rect.bottom - 80
        holder = Holder(Position(holder_x, holder_y), 50, "Support (stocker)", pygame.K_f, self.player)
        self.interactables.append(holder)

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update(self, dt: float):
        self._update_queue_positions()
        self.player.update(dt)

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

    def try_spawn(self, recipe):
        """Spawn a customer with the given recipe (called by Map for synchronized spawns)."""
        if len(self._customers) >= CUSTOMER_MAX_COUNT:
            return
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
        # Comptoir — at the top of the path, same width as the path
        pygame.draw.rect(self.screen, MAP_COMPTOIR_COLOR, self.comptoir_rect)

        # Order panel (fills the box — border drawn on top after)
        waiting = next((c for c in self._customers if c.is_waiting), None)
        self._draw_order_panel(waiting)

        # Box border drawn on top so it is never covered by the panel fill
        pygame.draw.rect(self.screen, MAP_SEPARATOR_COLOR, self.ingredient_box_rect, MAP_SEPARATOR_WIDTH)

        # Interactables
        for interactable in self.interactables:
            interactable.draw(self.screen)

        # Customers and player
        for customer in self._customers:
            customer.draw(self.screen)
        self.player.draw(self.screen)

    def _draw_order_panel(self, customer: Customer | None):
        global _FONT_TITLE, _FONT_BODY, _FONT_LABEL

        # ── Font loading (once) ───────────────────────────────────────────
        if _FONT_TITLE is None:
            try:
                _FONT_TITLE = pygame.font.Font(FONT_TITLE_PATH, 24)
            except Exception:
                _FONT_TITLE = pygame.font.SysFont('georgia', 24, bold=True)
        if _FONT_BODY is None:
            try:
                _FONT_BODY = pygame.font.Font(FONT_BODY_PATH, 18)
            except Exception:
                _FONT_BODY = pygame.font.SysFont('arial', 18)
        if _FONT_LABEL is None:
            try:
                _FONT_LABEL = pygame.font.Font(FONT_BODY_PATH, 13)
            except Exception:
                _FONT_LABEL = pygame.font.SysFont('arial', 13)

        box = self.ingredient_box_rect

        # ── Panel background ──────────────────────────────────────────────
        pygame.draw.rect(self.screen, _PANEL_BG, box)

        # ── Empty state ───────────────────────────────────────────────────
        if customer is None:
            msg  = _FONT_BODY.render("En attente d'un client...", True, (175, 148, 115))
            hint = _FONT_LABEL.render("La commande s'affichera ici", True, (200, 178, 150))
            self.screen.blit(msg,  msg.get_rect(center=(box.centerx, box.centery - 12)))
            self.screen.blit(hint, hint.get_rect(center=(box.centerx, box.centery + 14)))
            return

        recipe              = customer.recipe
        hdr_bg, hdr_txt     = _CAKE_PALETTE.get(recipe.cake_type, ((180, 120, 60), (255, 255, 255)))

        # ── Colored header with cake name ─────────────────────────────────
        HDR_H    = 46
        hdr_rect = pygame.Rect(box.left, box.top, box.width, HDR_H)
        pygame.draw.rect(self.screen, hdr_bg, hdr_rect)
        title_surf = _FONT_TITLE.render(recipe.cake_type.value, True, hdr_txt)
        self.screen.blit(title_surf, title_surf.get_rect(center=hdr_rect.center))

        # ── Ingredients section ───────────────────────────────────────────
        y = box.top + HDR_H + 10

        section_lbl = _FONT_LABEL.render("INGRÉDIENTS", True, (168, 138, 100))
        self.screen.blit(section_lbl, (box.left + _PAD, y))
        y += section_lbl.get_height() + 7

        BADGE_PX     = 9     # horizontal inner padding
        BADGE_PY     = 5     # vertical inner padding
        BADGE_GAP    = 6     # space between badges
        BADGE_RADIUS = 10

        x = box.left + _PAD
        for ingredient in recipe.ingredients:
            bg, fg = _INGREDIENT_PALETTE.get(ingredient, ((210, 210, 210), (50, 50, 50)))
            lbl    = _FONT_BODY.render(ingredient.value, True, fg)
            bw     = lbl.get_width()  + BADGE_PX * 2
            bh     = lbl.get_height() + BADGE_PY * 2

            # Wrap to next row if badge overflows the box
            if x + bw > box.right - _PAD:
                x  = box.left + _PAD
                y += bh + BADGE_GAP

            badge_rect = pygame.Rect(x, y, bw, bh)
            pygame.draw.rect(self.screen, bg, badge_rect, border_radius=BADGE_RADIUS)
            self.screen.blit(lbl, (x + BADGE_PX, y + BADGE_PY))
            x += bw + BADGE_GAP

        bh_last = _FONT_BODY.get_height() + BADGE_PY * 2
        y += bh_last + 10

        # ── Reward (right-aligned, with drawn star) ───────────────────────
        pts_surf = _FONT_BODY.render(f"{recipe.reward} pts", True, (185, 140, 0))
        pts_rect = pts_surf.get_rect(right=box.right - _PAD, y=y)
        self.screen.blit(pts_surf, pts_rect)
        _draw_star(self.screen, pts_rect.left - 14, pts_rect.centery, 10, (215, 168, 0))

        # ── Patience bar ──────────────────────────────────────────────────
        BAR_H   = 22
        bar_bg  = pygame.Rect(box.left, box.bottom - BAR_H, box.width, BAR_H)
        pygame.draw.rect(self.screen, (212, 202, 188), bar_bg)

        # Smooth color: green → yellow → red as patience depletes
        ratio = customer.patience_ratio
        if ratio >= 0.5:
            t = (1.0 - ratio) * 2       # 0.0 → 1.0 as ratio goes 1.0 → 0.5
            r, g = int(t * 255), 195
        else:
            t = ratio * 2               # 1.0 → 0.0 as ratio goes 0.5 → 0.0
            r, g = 255, int(t * 195)

        fill_rect = pygame.Rect(box.left, box.bottom - BAR_H, int(box.width * ratio), BAR_H)
        pygame.draw.rect(self.screen, (r, g, 0), fill_rect)

        # Time remaining text over the bar
        time_surf = _FONT_LABEL.render(f"{int(customer.patience)}s", True, (30, 18, 8))
        self.screen.blit(time_surf, time_surf.get_rect(centery=bar_bg.centery, x=box.left + 8))

    def handle_keydown(self, key):
        """Gère les touches pressées pour les interactables"""
        for interactable in self.interactables:
            if hasattr(interactable, "handle_keydown"):
                interactable.handle_keydown(key)

    def handle_movement(self, keys: list[bool]):
        """Gère les touches de mouvement pour le joueur"""
        self.player.handle_movement(keys)

    def handle_events(self):
        for interactable in self.interactables:
            if hasattr(interactable, "handle_events") and callable(getattr(interactable, "handle_events")):
                interactable.handle_events()

        self.player.handle_events()