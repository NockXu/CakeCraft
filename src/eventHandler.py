import pygame

class eventHandler:
    def __init__(self):
        self._thingToHandle = []

    def add_thing(self, thing):
        if hasattr(thing, "handle_events") and callable(getattr(thing, "handle_events")):
            self._thingToHandle.append(thing)

    def remove_thing(self, thing):
        if thing in self._thingToHandle:
            self._thingToHandle.remove(thing)

    def add_things(self, things):
        for thing in things:
            self.add_thing(thing)
    
    def remove_things(self, things):
        for thing in things:
            self.remove_thing(thing)
    
    def handle_events(self, keys):
        for thing in self._thingToHandle:
            thing.handle_events(keys)