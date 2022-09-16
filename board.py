from flask import Flask, request, render_template
from piece import *
from player import *

class Board:
    def __init__(self):
        self.positions = [
            W_ROOK, W_KNIGHT, W_BISHOP, W_QUEEN, W_KING, W_BISHOP, W_KNIGHT, W_ROOK,
            W_PAWN, W_PAWN,   W_PAWN,   W_PAWN,  W_PAWN, W_PAWN,   W_PAWN,   W_PAWN, 
            EMPTY,  EMPTY,    EMPTY,    EMPTY,   EMPTY,  EMPTY,    EMPTY,    EMPTY,
            EMPTY,  EMPTY,    EMPTY,    EMPTY,   EMPTY,  EMPTY,    EMPTY,    EMPTY,
            EMPTY,  EMPTY,    EMPTY,    EMPTY,   EMPTY,  EMPTY,    EMPTY,    EMPTY,
            EMPTY,  EMPTY,    EMPTY,    EMPTY,   EMPTY,  EMPTY,    EMPTY,    EMPTY,
            B_PAWN, B_PAWN,   B_PAWN,   B_PAWN,  B_PAWN, B_PAWN,   B_PAWN,   B_PAWN, 
            B_ROOK, B_KNIGHT, B_BISHOP, B_QUEEN, B_KING, B_BISHOP, B_KNIGHT, B_ROOK,
        ]

        self.white_piece = None
        self.black_piece = None

        self.create_table()

    def create_table(self):
        # White pieces
        p = King(4, W_KING, WHITE, "/static/king_white.png")
        self.white_piece = p
        for i in range(8):
            p.next = Pawn(8+i, W_PAWN, WHITE, "/static/pawn_white.png")
            p = p.next
        p.next = Queen(3, W_QUEEN, WHITE, "/static/queen_white.png")
        p = p.next
        p.next = Rook(0, W_ROOK, WHITE, "/static/rook_white.png")
        p = p.next
        p.next = Rook(7, W_ROOK, WHITE, "/static/rook_white.png")
        p = p.next
        p.next = Knight(1, W_KNIGHT, WHITE, "/static/knight_white.png")
        p = p.next
        p.next = Knight(6, W_KNIGHT, WHITE, "/static/knight_white.png")
        p = p.next
        p.next = Bishop(2, W_BISHOP, WHITE, "/static/bishop_white.png")
        p = p.next
        p.next = Bishop(5, W_BISHOP, WHITE, "/static/bishop_white.png")

        # Black pieces
        p = King(60, B_KING, BLACK, "/static/king_black.png")
        self.black_piece = p
        for i in range(8):
            p.next = Pawn(48+i, B_PAWN, BLACK, "/static/pawn_black.png")
            p = p.next
        p.next = Queen(59, B_QUEEN, BLACK, "/static/queen_black.png")
        p = p.next
        p.next = Rook(56, B_ROOK, BLACK, "/static/rook_black.png")
        p = p.next
        p.next = Rook(63, B_ROOK, BLACK, "/static/rook_black.png")
        p = p.next
        p.next = Knight(57, B_KNIGHT, BLACK, "/static/knight_black.png")
        p = p.next
        p.next = Knight(62, B_KNIGHT, BLACK, "/static/knight_black.png")
        p = p.next
        p.next = Bishop(58, B_BISHOP, BLACK, "/static/bishop_black.png")
        p = p.next
        p.next = Bishop(61, B_BISHOP, BLACK, "/static/bishop_black.png")

    def move_sel_up(self):
        self.sel_idx += 8

    def move_sel_down(self):
        self.sel_idx -= 8

    def move_sel_right(self):
        self.sel_idx += 1
    
    def move_sel_left(self):
        self.sel_idx -= 1

    def possible_moves(self, piece):
        result = []
        possible_moves = piece.possible_moves()

        if (piece.type in PAWN):
            x = piece.idx % 8
            for i in range(len(possible_moves)):
                n = possible_moves[i]
                x_n = n % 8         
                if (x == x_n and self.positions[n] == EMPTY):
                    result.append(n)
                elif ((piece.color == WHITE and self.positions[n] < EMPTY) or
                      (piece.color == BLACK and self.positions[n] > EMPTY)):
                    result.append(n)

        elif (piece.type in KING):
            print("")
        else:
            print(possible_moves)
            for i in range(len(possible_moves)):
                n = possible_moves[i]
                if ((piece.color == WHITE and self.positions[n] <  1) or
                    (piece.color == BLACK and self.positions[n] > -1)):
                    result.append(n)

        return result            

board = Board()
player = Player()

# Routes
app = Flask(__name__)
@app.route('/')
def board_create():
    return render_template('index.html')

@app.route('/move', methods=["POST"])
def move():
    sel_idx = 63 - request.get_json()['sel_idx']

    p = board.white_piece
    if (player.color == BLACK): p = board.black_piece
    while (p and p.idx != sel_idx): p = p.next
    
    possible = board.possible_moves(p)
    str_possible = ""
    for i in range(len(possible)):
        str_possible += str(63 - possible[i]) + ","
    str_possible = str_possible[:-1]

    move = '{"possible_moves": "' + str_possible + '"}'

    return move

@app.route('/complete_move', methods=["POST"])
def complete_move():
    sel_idx   = 63 - request.get_json()['sel_idx']
    sel_piece = 63 - request.get_json()['sel_piece']

    p = board.white_piece
    p_opposite = board.black_piece
    if (player.color == BLACK):
        p = board.black_piece
        p_opposite = board.white_piece
    while (p and p.idx != sel_piece):
        p = p.next

    # Move piece
    board.positions[p.idx] = EMPTY
    p.idx = sel_idx
    board.positions[p.idx] = p.type

    if (p.type in PAWN or p.type in KING or p.type in ROOK):
        p.not_moved = False

    # In case of capture, remove captured piece from the board
    while (p_opposite and p_opposite.idx != sel_idx):
        p_opposite = p_opposite.next
    if (p_opposite):
        p_opposite.captured = True

    player.change_color()

    status = '{"status": "ok"}'

    return status