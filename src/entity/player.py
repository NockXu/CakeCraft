import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from entity.entity import Entity
from position import Position
import pygame
from constants import PLAYER_SIZE, PLAYER_SPRITE_PATH, PLAYER_SPRITE_SCALE, PLAYER_ANIM_FPS, PLAYER_SPEED


# Sprite sheet row indices (RPG Maker VX format)
_DIR_DOWN  = 0   # facing camera
_DIR_LEFT  = 1
_DIR_RIGHT = 2
_DIR_UP    = 3   # back to camera

_COLS = 3   # frames per row
_ROWS = 4   # directions

# Module-level cache — sprite loaded once, shared by all Player instances
_frames: list[list[pygame.Surface]] = []   # [direction][frame_index]


def _load_sprites():
    """Load and slice the sprite sheet into individual frames (called once)."""
    global _frames
    if _frames:
        return
    try:
        sheet    = pygame.image.load(PLAYER_SPRITE_PATH).convert_alpha()
        frame_w  = sheet.get_width()  // _COLS
        frame_h  = sheet.get_height() // _ROWS
        scale    = PLAYER_SPRITE_SCALE
        ratio    = scale / frame_h
        new_w    = int(frame_w * ratio)
        _frames  = []
        for row in range(_ROWS):
            row_frames = []
            for col in range(_COLS):
                raw    = sheet.subsurface(col * frame_w, row * frame_h, frame_w, frame_h)
                scaled = pygame.transform.scale(raw, (new_w, scale))
                row_frames.append(scaled)
            _frames.append(row_frames)
    except Exception:
        _frames = []   # fallback to colored rect if loading fails


class Player(Entity):
    def __init__(self, position: Position, size: int = PLAYER_SIZE,
                 color: tuple = (255, 0, 0), boundary: pygame.Rect = None,
                 controls: dict = None):
        super().__init__(position)
        self.size     = size
        self.color    = color
        self.boundary = boundary
        self.controls = controls

        # Animation state
        self._direction  = _DIR_DOWN   # current facing direction (row index)
        self._frame_idx  = 1           # 0-2; 1 = neutral/idle
        self._anim_timer = 0.0
        self._is_moving  = False       # set by move(), reset by update()

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------

    def move(self, dx: int, dy: int):
        super().move(dx, dy)
        if self.boundary:
            half = self.size // 2
            self.position.x = max(self.boundary.left  + half,
                                  min(self.position.x, self.boundary.right  - half))
            self.position.y = max(self.boundary.top   + half,
                                  min(self.position.y, self.boundary.bottom - half))

        # Determine facing direction (vertical movement takes priority)
        if dy < 0:
            self._direction = _DIR_UP
        elif dy > 0:
            self._direction = _DIR_DOWN
        elif dx < 0:
            self._direction = _DIR_LEFT
        elif dx > 0:
            self._direction = _DIR_RIGHT

        self._is_moving = True

    # ------------------------------------------------------------------
    # Animation update (call once per frame from PlayerZone.update)
    # ------------------------------------------------------------------

    def update(self, dt: float):
        if self._is_moving:
            self._anim_timer += dt
            if self._anim_timer >= 1.0 / PLAYER_ANIM_FPS:
                self._anim_timer = 0.0
                self._frame_idx  = (self._frame_idx + 1) % _COLS
        else:
            # Idle — hold the neutral (middle) frame
            self._frame_idx  = 1
            self._anim_timer = 0.0

        # Reset every frame; move() sets it again if a key is still held
        self._is_moving = False

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------

    def draw(self, screen: pygame.Surface):
        _load_sprites()

        if _frames:
            frame = _frames[self._direction][self._frame_idx]
            x = int(self.position.x) - frame.get_width()  // 2
            y = int(self.position.y) - frame.get_height() // 2
            screen.blit(frame, (x, y))
        else:
            # Fallback: colored rectangle if sprite failed to load
            pygame.draw.rect(screen, self.color,
                             (self.position.x - self.size // 2,
                              self.position.y - self.size // 2,
                              self.size, self.size))

        for child in self.children:
            child.draw(screen)
    
    def pick_up_cake(self, cake):
        """Le joueur prend un gâteau"""
        if cake not in self.children:
            self.add_child(cake)
            cake.carried_by = self
            return True
        return False
    
    def drop_cake(self, cake):
        """Le joueur lâche un gâteau"""
        if cake in self.children:
            self.remove_child(cake)
            cake.carried_by = None
            return True
        return False
    
    def drop_all_cakes(self):
        """Le joueur lâche tous les gâteaux"""
        for child in self.children[:]:
            self.drop_cake(child)
    
    def get_carried_cakes(self):
        """Retourne la liste des gâteaux portés"""
        return self.children.copy()
    
    def handle_events(self, keys):
        """Gère les événements de mouvement selon le joueur"""
        if keys[self.controls["left"]]:
            self.move(-PLAYER_SPEED, 0)
        if keys[self.controls["right"]]:
            self.move(PLAYER_SPEED, 0)
        if keys[self.controls["up"]]:
            self.move(0, -PLAYER_SPEED)
        if keys[self.controls["down"]]:
            self.move(0, PLAYER_SPEED)
