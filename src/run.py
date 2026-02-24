import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from map.map import Map
from constants import FPS, TIME_FAST_FORWARD_SCALE
from eventHandler import eventHandler

class Game:
    def __init__(self):
        pygame.init()
        self.map = Map()
        self.eventHandler = eventHandler()
        self.eventHandler.add_thing(self.map.zone_left)
        self.eventHandler.add_thing(self.map.zone_right)
        self.clock = pygame.time.Clock()
        self.running = True
    
    def _time_scale(self) -> float:
        """Returns a time multiplier — hold TAB to fast-forward."""
        keys = pygame.key.get_pressed()
        return TIME_FAST_FORWARD_SCALE if keys[pygame.K_TAB] else 1.0
    
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0 * self._time_scale()
            
            # Gérer les événements de base (QUIT, ESCAPE) et les touches spécifiques
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    else:
                        # Envoyer l'événement de touche spécifique aux interactables
                        self.eventHandler.handle_keydown(event.key)
            
            # Pour le mouvement continu, on garde les touches pressées
            keys = pygame.key.get_pressed()
            self.eventHandler.handle_movement(keys)

            self.eventHandler.handle_events()

            self.map.update(dt)
            self.map.draw()
            
            if not self.map.running:
                self.running = False
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
