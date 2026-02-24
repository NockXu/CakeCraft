import sys
import pygame
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from entity.item.item import Item
from position import Position

class Test(Item):
    def __init__(self):
        super().__init__(Position(0, 0), "Test", 20, (255, 0, 0))