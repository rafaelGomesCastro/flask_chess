from operator import truediv
from sre_constants import NOT_LITERAL
from player import *

# Pieces
W_PAWN   = 1
W_ROOK   = 2
W_KNIGHT = 3
W_BISHOP = 4
W_QUEEN  = 5
W_KING   = 6

EMPTY    = 0

B_PAWN   = -1
B_ROOK   = -2
B_KNIGHT = -3
B_BISHOP = -4
B_QUEEN  = -5
B_KING   = -6

PAWN   = [W_PAWN, B_PAWN]
ROOK   = [W_ROOK, B_ROOK]
KNIGHT = [W_KNIGHT, B_KNIGHT]
BISHOP = [W_BISHOP, B_BISHOP]
QUEEN  = [W_QUEEN, B_QUEEN]
KING   = [W_KING, B_KING]

class Piece:
    def __init__(self, idx, type, color, img_url):
        self.idx     = idx
        self.type    = type
        self.color   = color
        self.img_url = img_url
        self.in_game = True

        self.next    = None

    def set_idx(self, idx):
        self.idx = idx

    def captured(self):
        self.in_game = False

class King(Piece):
    def __init__(self, idx, type, color, img_url):
        super().__init__(idx, type, color, img_url)

        self.not_moved = True
    
    def possible_moves(self):
        x = self.idx % 8
        y = int(self.idx / 8)

        result = []
        if ((x+1) <  8): result.append(y*8 + (x+1))
        if ((x-1) > -1): result.append(y*8 + (x-1))
        if ((y+1) <  8): result.append((y+1)*8 + x)
        if ((y-1) > -1): result.append((y-1)*8 + x)
        if ((x+1) <  8 and (y+1) <  8): result.append((y+1)*8 + (x+1))
        if ((x+1) <  8 and (y-1) > -1): result.append((y-1)*8 + (x+1))
        if ((x-1) > -1 and (y+1) <  8): result.append((y+1)*8 + (x-1))
        if ((x-1) > -1 and (y-1) > -1): result.append((y-1)*8 + (x-1))

        if (self.not_moved):
            result.append(self.idx + 2)
            result.append(self.idx - 2)

        return result

class Bishop(Piece):
    def possible_moves(self):
        result = []

        x = self.idx % 8
        y = int(self.idx / 8)
        while (x < 8 and y < 8):
            result.append((y+1)*8 + (x+1))
            x += 1
            y += 1

        x = self.idx % 8
        y = int(self.idx / 8)
        while (x < 8 and y > -1):
            result.append((y+1)*8 + (x-1))
            x += 1
            y -= 1

        x = self.idx % 8
        y = int(self.idx / 8)
        while (x > -1 and y < 8):
            result.append((y+1)*8 + (x-1))
            x -= 1
            y += 1

        x = self.idx % 8
        y = int(self.idx / 8)
        while (x > -1 and y > -1):
            result.append((y-1)*8 + (x-1))
            x -= 1
            y -= 1

        return result

class Rook(Piece):
    def __init__(self, idx, type, color, img_url):
        super().__init__(idx, type, color, img_url)

        self.not_moved = True

    def possible_moves(self):
        result = []

        x = self.idx % 8
        y = int(self.idx / 8)
        while ((x+1) <  8):
            result.append(y*8 + (x+1))
            x += 1
        x = self.idx % 8
        while ((x-1) > -1):
            result.append(y*8 + (x-1))
            x -= 1
        x = self.idx % 8
        while ((y+1) <  8):
            result.append((y+1)*8 + x)
            y += 1
        y = int(self.idx / 8)
        while ((y-1) > -1):
            result.append((y-1)*8 + x)
            y -= 1
        
        return result

class Queen(Piece):
    def possible_moves(self):
        result = []

        x = self.idx % 8
        y = int(self.idx / 8)
        while (x < 8 and y < 8):
            result.append((y+1)*8 + (x+1))
            x += 1
            y += 1

        x = self.idx % 8
        y = int(self.idx / 8)
        while (x < 8 and y > -1):
            result.append((y+1)*8 + (x-1))
            x += 1
            y -= 1

        x = self.idx % 8
        y = int(self.idx / 8)
        while (x > -1 and y < 8):
            result.append((y+1)*8 + (x-1))
            x -= 1
            y += 1

        x = self.idx % 8
        y = int(self.idx / 8)
        while (x > -1 and y > -1):
            result.append((y-1)*8 + (x-1))
            x -= 1
            y -= 1

        x = self.idx % 8
        y = int(self.idx / 8)
        while ((x+1) <  8):
            result.append(y*8 + (x+1))
            x += 1
        x = self.idx % 8
        while ((x-1) > -1):
            result.append(y*8 + (x-1))
            x -= 1
        x = self.idx % 8
        while ((y+1) <  8):
            result.append((y+1)*8 + x)
            y += 1
        y = int(self.idx / 8)
        while ((y-1) > -1):
            result.append((y-1)*8 + x)
            y -= 1
        
        return result

class Knight(Piece):
    def possible_moves(self):
        result = []

        x = self.idx % 8
        y = int(self.idx / 8)
        if ((x+1) <  8 and (y+2) <  8): result.append((y+2)*8 + (x+1))
        if ((x+2) <  8 and (y+1) <  8): result.append((y+1)*8 + (x+2))
        if ((x+1) <  8 and (y-2) > -1): result.append((y-2)*8 + (x+1))
        if ((x+2) <  8 and (y-1) > -1): result.append((y-1)*8 + (x+2))
        if ((x-1) > -1 and (y+2) <  8): result.append((y+2)*8 + (x-1))
        if ((x-2) > -1 and (y+1) <  8): result.append((y+1)*8 + (x-2))
        if ((x-1) > -1 and (y-2) > -1): result.append((y-2)*8 + (x-1))
        if ((x-2) > -1 and (y-1) > -1): result.append((y-1)*8 + (x-2))

        return result

class Pawn(Piece):
    def __init__(self, idx, type, color, img_url):
        super().__init__(idx, type, color, img_url)

        self.not_moved = True
    
    def possible_moves(self):
        result = []

        x = self.idx % 8
        y = int(self.idx / 8)
        if (self.type == W_PAWN):
            result.append((y+1)*8 + x)
            if ((x+1) <  8): result.append((y+1)*8 + (x+1))
            if ((x-1) > -1): result.append((y+1)*8 + (x-1))
            if (self.not_moved): result.append((y+2)*8 + x)
        else:
            result.append((y-1)*8 + x)
            if ((x+1) <  8): result.append((y-1)*8 + (x+1))
            if ((x-1) > -1): result.append((y-1)*8 + (x-1))
            if (self.not_moved): result.append((y-2)*8 + x)

        return result