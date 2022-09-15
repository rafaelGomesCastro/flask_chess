# Colors
WHITE = 0
BLACK = 1

class Player:
    def __init__(self):
        self.color = WHITE


    def change_color(self):
        self.color = (self.color) + 1 % 2