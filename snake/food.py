import numpy
import random

class Food:
    def __init__(self, board_size, x=None, y=None):
        self.board_size = board_size
        if x is None and y is None:
            self.respawn()
        else:
            self.x = x
            self.y = y
        
    
    def respawn(self):
        self.x = random.randint(0, self.board_size)
        self.y = random.randint(0, self.board_size)