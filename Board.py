from __future__ import annotations
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
from Piece import Piece
from Piece import Empty
from Piece import King
from Piece import Queen
from Piece import Pawn
from Piece import Knight
from Piece import Bishop
from Piece import Rook
from Move import Move
from Conditions import Conditions
import math
import copy

BASE_Y = 100
BASE_X = 220
INCREMENT = 16

class Board:
    def __init__(self, width:int, height:int, white_icon:str="", black_icon:str=""):
        self.board:list[list[Piece]] = []
        self.width = width-1
        self.height = height-1
        self.teams:list[Team] = []

        self.focus_piece:Piece = ""
        self.focus_moves:list[Move] = ""

        self.turn = 1

        self.white = white_icon
        self.black = black_icon

        self.empty_board:list[list[str]] = []

        for y in range(height):
            row = []
            empty_row = []

            for x in range(width):
                row.append(Empty(self, x, y, "null"))

                if y%2 == 1:
                    if x%2 == 1:
                        empty_row.append(self.black)
                    else:
                        empty_row.append(self.white)
                else:
                    if x%2 == 1:
                        empty_row.append(self.white)
                    else:
                        empty_row.append(self.black)

            self.board.append(row)
            self.empty_board.append(empty_row)


    def update(self):
        for team in self.teams:
            for piece in team.team:
                self.board[piece.y][piece.x] = piece
                piece.icon.center_x = (piece.x * INCREMENT) + BASE_X
                piece.icon.center_y = (piece.y * INCREMENT) + BASE_Y

            x = BASE_X
            for piece in team.captured:
                if piece.direction == 1:
                    y = (-2 * INCREMENT) + BASE_Y
                elif piece.direction == -1:
                    y = (9 * INCREMENT) + BASE_Y

                piece.icon.center_x = x
                piece.icon.center_y = y

                x += INCREMENT

        for team in self.teams:
            for piece in team.team:
                piece.update_possible_moves()

        for team in self.teams:
            for piece in team.team:
                if piece.crucial:
                    if Conditions.is_in_check(piece):
                        for piece_ in piece.team.team:
                            new_moves = []
                            for move in piece_.possible_moves:
                                stops_check = self.test_move_check(piece_, move[0], move[1], move[2], piece)
                                if stops_check:
                                    new_moves.append(move)
                            piece_.possible_moves = new_moves

    def add_team(self, team:Team):
        self.teams.append(team)

    def temp_remove(self, piece:Piece):
        self.board[piece.y][piece.x] = Empty(self, piece.x, piece.y, "null")
        # print("test")
    def re_add(self, piece):
        self.board[piece.y][piece.x] = piece

    def add_piece(self, x:int, y:int, piece:Piece):
        self.board[y][x] = piece
    def remove_piece(self, x:int, y:int, piece:Piece):
        self.board[y][x] = Empty()

    def get_piece(self, piece:Piece, x_offset:int, y_offset:int):
        x:int = piece.x + (x_offset)
        y:int = piece.y + (y_offset)
        return self.board[y][x]

    def test_move_check(self, piece:Piece, x:int, y:int, move:Move, checked:Piece=None):
        if checked == None:
            checked = piece

        hypothetical_board = copy.deepcopy(self)
        hypo_piece = hypothetical_board.board[piece.y][piece.x]
        hypo_checked = hypothetical_board.board[checked.y][checked.x]

        hypothetical_board.move_piece(hypo_piece, x, y, move, True)

        stops_check = not Conditions.is_in_check(hypo_checked)
        return stops_check

    def move_piece(self, piece:Piece, x:int, y:int, move:Move, skip_update:bool=False):
        move.run(piece)

        spot = self.board[y][x]

        self.board[y][x] = piece
        self.board[piece.y][piece.x] = Empty(self, piece.x, piece.y, "null")

        piece.x = x
        piece.y = y

        if not isinstance(spot, Empty):
            piece.team.captured
            spot.team.captured.append(spot)
            spot.team.team.remove(spot)

        piece.times_moved += 1

        if not skip_update:
            self.update()

        self.turn *= -1

    def move(self, piece:Piece, x:int, y:int):
            spot = self.board[y][x]
    
            self.board[y][x] = piece
            self.board[piece.y][piece.x] = Empty(self, piece.x, piece.y, "null")
    
            piece.x = x
            piece.y = y
    
            if not isinstance(spot, Empty):
                spot.team.captured.append(spot)
                spot.team.team.remove(spot)
    
            self.update()


    # Helpers
    def get_captures(self, piece:Piece, get_empty_slots:bool=False):
        captures:list[Piece] = []

        for move in piece.possible_moves:
            check = self.board[move[1]][move[0]]
            if not isinstance(check, Empty) or get_empty_slots:
                captures.append(check)

        return captures

    
    def get_path_between(self, base_piece:Piece, piece:Piece):
        if base_piece.x >= piece.x:
            big_x = base_piece.x
            small_x = piece.x
        else:
            big_x = piece.x
            small_x = base_piece.x

        if base_piece.y >= piece.y:
            big_y = base_piece.y
            small_y = piece.y
        else:
            big_y = piece.y
            small_y = base_piece.y

        r_list:list[Piece] = []

        # horizontal
        if base_piece.x == piece.x and base_piece.y != piece.y:
            for check_y in range(small_y+1, big_y):
                r_list.append(self.board[check_y][piece.x])

        # vertical  
        elif base_piece.y == piece.y and base_piece.x != piece.x:
            for check_x in range(small_x+1, big_x):
                r_list.append(self.board[piece.y][check_x])

        # diagnal
        elif math.abs(base_piece.x - piece.x) == math.abs(base_piece.y - piece.y):
            for check in range(small_x+1, big_x):
                # up
                if base_piece.y > piece.y:
                    r_list.append(self.board[check][check])
                # down
                else:
                    r_list.append(self.board[-check][check])

        return r_list


class StandardBoard(Board):
    def __init__(self):
        super().__init__(8, 8, "icons/white.png", "icons/black.png")

        black = Team("Black", self)
        black.team = [
            Rook(self, 0, 0, black, icon="icons/black/rook.png"),
            Knight(self, 1, 0, black, icon="icons/black/knight.png"),
            Bishop(self, 2, 0, black, icon="icons/black/bishop.png"),
            Queen(self, 3, 0, black, icon="icons/black/queen.png"),
            King(self, 4, 0, black, icon="icons/black/king.png"),
            Bishop(self, 5, 0, black, icon="icons/black/bishop.png"),
            Knight(self, 6, 0, black, icon="icons/black/knight.png"),
            Rook(self, 7, 0, black, icon="icons/black/rook.png"),

            Pawn(self, 0, 1, black, icon="icons/black/pawn.png"),
            Pawn(self, 1, 1, black, icon="icons/black/pawn.png"),
            Pawn(self, 2, 1, black, icon="icons/black/pawn.png"),
            Pawn(self, 3, 1, black, icon="icons/black/pawn.png"),
            Pawn(self, 4, 1, black, icon="icons/black/pawn.png"),
            Pawn(self, 5, 1, black, icon="icons/black/pawn.png"),
            Pawn(self, 6, 1, black, icon="icons/black/pawn.png"),
            Pawn(self, 7, 1, black, icon="icons/black/pawn.png")
        ]

        white = Team("White", self)
        white.team = [
            Rook(self, 0, 7, white, -1, icon="icons/white/rook.png"),
            Knight(self, 1, 7, white, -1, icon="icons/white/knight.png"),
            Bishop(self, 2, 7, white, -1, icon="icons/white/bishop.png"),
            Queen(self, 4, 7, white, -1, icon="icons/white/queen.png"),
            King(self, 3, 7, white, -1, icon="icons/white/king.png"),
            Bishop(self, 5, 7, white, -1, icon="icons/white/bishop.png"),
            Knight(self, 6, 7, white, -1, icon="icons/white/knight.png"),
            Rook(self, 7, 7, white, -1, icon="icons/white/rook.png"),

            Pawn(self, 0, 6, white, -1, icon="icons/white/pawn.png"),
            Pawn(self, 1, 6, white, -1, icon="icons/white/pawn.png"),
            Pawn(self, 2, 6, white, -1, icon="icons/white/pawn.png"),
            Pawn(self, 3, 6, white, -1, icon="icons/white/pawn.png"),
            Pawn(self, 4, 6, white, -1, icon="icons/white/pawn.png"),
            Pawn(self, 5, 6, white, -1, icon="icons/white/pawn.png"),
            Pawn(self, 6, 6, white, -1, icon="icons/white/pawn.png"),
            Pawn(self, 7, 6, white, -1, icon="icons/white/pawn.png")
        ]

        self.teams = [white, black]

        self.update()





class Team:
    def __init__(self, name:str, board:Board, team:list[Piece]=None, captured:list[Piece]=None):
        if team == None:
            team = []
        if captured == None:
            captured = []
        
        self.name:str = name
        self.team:list[Piece] = team
        self.board:Board = board
        self.captured:list[Piece] = captured