import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from entity.entity import Entity
from position import Position
from recipe import Recipe
from enums import CustomerState
from constants import CUSTOMER_SIZE, CUSTOMER_SPEED, CUSTOMER_COLOR, CUSTOMER_ANGRY_COLOR
import pygame


class Customer(Entity):
    def __init__(self, position: Position, wait_position: Position, leave_position: Position, recipe: Recipe):
        super().__init__(position)
        self.wait_position  = wait_position
        self.leave_position = leave_position
        self.recipe         = recipe
        self.state          = CustomerState.WALKING
        self.patience       = recipe.time_limit

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update(self, dt: float):
        if self.state == CustomerState.WALKING:
            self._walk_toward(self.wait_position, dt)
            if self._reached(self.wait_position):
                self.state = CustomerState.QUEUED

        elif self.state == CustomerState.QUEUED:
            # Keep moving toward wait_position — it shifts as the queue advances
            if not self._reached(self.wait_position):
                self._walk_toward(self.wait_position, dt)
            # Promotion to WAITING is handled by PlayerZone once at front

        elif self.state == CustomerState.WAITING:
            self.patience -= dt
            if self.patience <= 0:
                self.state = CustomerState.LEAVING

        elif self.state in (CustomerState.SERVED, CustomerState.LEAVING):
            self._walk_toward(self.leave_position, dt)

    def serve(self):
        """Call this when the player successfully delivers the order."""
        self.state = CustomerState.SERVED

    @property
    def patience_ratio(self) -> float:
        return max(0.0, self.patience / self.recipe.time_limit)

    @property
    def is_waiting(self) -> bool:
        return self.state == CustomerState.WAITING

    @property
    def is_done(self) -> bool:
        """True once the customer has fully left and can be removed."""
        return self.state in (CustomerState.SERVED, CustomerState.LEAVING) and self._reached(self.leave_position)

    # ------------------------------------------------------------------
    # Draw — only the customer sprite (order panel is drawn by PlayerZone)
    # ------------------------------------------------------------------

    def draw(self, screen: pygame.Surface):
        x, y  = int(self.position.x), int(self.position.y)
        color = CUSTOMER_ANGRY_COLOR if self.state == CustomerState.LEAVING else CUSTOMER_COLOR
        pygame.draw.circle(screen, color, (x, y), CUSTOMER_SIZE)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _walk_toward(self, target: Position, dt: float):
        """Move toward target in 2D at CUSTOMER_SPEED px/s."""
        dx   = target.x - self.position.x
        dy   = target.y - self.position.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        step = CUSTOMER_SPEED * dt
        if dist <= step:
            self.position.x = target.x
            self.position.y = target.y
        else:
            factor           = step / dist
            self.position.x += dx * factor
            self.position.y += dy * factor

    def _reached(self, target: Position) -> bool:
        dx = target.x - self.position.x
        dy = target.y - self.position.y
        return (dx ** 2 + dy ** 2) ** 0.5 < 1
