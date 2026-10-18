from __future__ import annotations
from typing import TYPE_CHECKING, Protocol
if TYPE_CHECKING:
    from Piece import Piece, Empty, can_castle
from Board import *
import math

# direction is used in order to help keep track of proper offsetting without having to creat two Move variants of the same kind of move but for different sides of the board

class Conditions:
    # Common conditions
    def pawn_forward(piece:Piece):
        x = piece.x
        y = piece.y + (piece.direction * 1)
        if piece.board.board[y][x].name == "empty":
            return True
        else:
            return False
        
    def pawn_start(piece:Piece):
        if Conditions.pawn_forward(piece):
            x = piece.x
            y = piece.y + (piece.direction * 2)
            if piece.board.board[y][x].name == "empty":
                return Conditions.special_move_(piece, Conditions.move_limit)

        return False
        
    def pawn_left_capture(piece:Piece):
        return Conditions.special_capture(piece, piece.direction * -1, piece.direction * 1)
    
    def pawn_right_capture(piece:Piece):
        return Conditions.special_capture(piece, piece.direction * 1, piece.direction * 1)
        

    def king_side_castle(piece:can_castle):
        if piece.times_moved == 0:
            castler:Piece = piece.board.get_piece(piece, 3, 0)
            return Conditions.castle(piece, castler)
        else:
            return False
    
    def queen_side_castle(piece:can_castle):
        if piece.times_moved == 0:
            castler:Piece = piece.board.get_piece(piece, -4, 0)
            return Conditions.castle(piece, castler)
        else: 
            return False

    def castle(piece, castler):
        # other piece has never moved
        if castler.times_moved == 0:
            # no pieces between them
            if Conditions.clear_shot(piece, castler):
                # King cannot be in check, move through check, or end in check
                if piece.crucial:
                    check = False

                    # end in check
                    if Conditions.is_in_check(castler):
                        check = True
                    # go through check
                    checks = piece.board.get_path_between(piece, castler)
                    for check_piece in checks:
                        if Conditions.is_in_check(check_piece, piece):
                            check = True
                    # be in check
                    if Conditions.is_in_check(piece):
                        check = True

                    if not check:
                        return True
                else:
                    return True
                
        return False

    # General conditions for repeated use
    def special_move(piece:Piece, x:int, y:int, condition):
        if condition(piece, x, y):
            return True
        
        return False
    # Overriding is based on order and previous functions can't be accessed in Python
    def special_move_(piece:Piece, condition):
        if condition(piece):
            return True
        
        return False
    
    def special_capture(piece:Piece, x_target:int, y_target:int):
        return Conditions.special_move(piece, x_target, y_target, Conditions.capture)

    def capture(piece:Piece, x:int, y:int):
        if piece.in_bounds(piece.x + x, piece.y + y):
            target:Piece = piece.board.get_piece(piece, x, y)

            if target.name != "empty":
                if not target.ally(piece):
                    return True
        
        return False

    def move_limit(piece:Piece, move_limit:int=1):
        if piece.times_moved < move_limit:
            return True

        return False


    # Helpers
    def is_in_check(piece:Piece, base_piece=None):
        for team in piece.board.teams:
            if piece.team == "null":
                team_ = "null"
            else:
                team_ = piece.team.name

            if base_piece == None:
                check_name = None
            else:
                check_name = base_piece.team.name

            if team.name != team_ and team.name != check_name:
                for other in team.team:
                    for move in other.possible_moves:
                        if piece.x == move[0] and piece.y == move[1]:
                            return True

        return False

    def distance_between(base_piece:Piece, piece:Piece):
        # a**2 + b**2 = c**2
        # c = (a**2 + b**2)**.5
        a = math.abs(base_piece.x - piece.x)
        b = math.abs(base_piece.y - piece.y)
        distance = (a**2 + b**2)**.5
        return distance

    # Checks that spots between two pieces are clear
    def clear_shot(base_piece:Piece, piece:Piece):
        for check in base_piece.board.get_path_between(base_piece, piece):
            if check.name != "empty":
                return False

        return True


# Many special moves involve an extra moving of a piece that can be hard to take into account with turns. Using this class can implement extra functions that are ran alongside a particular move
class ExtraFunctions:
    def move_other(piece, offset_x, offset_y, direction=True):
        # castling direction is the same on either side of the board but the directional usage for my pawn capture functions require the direction to flip
        if direction:
            offset_x = offset_x * piece.direction
            offset_y = offset_y * piece.direction

        x = piece.x + offset_x
        y = piece.y + offset_y

        if piece.board.board[y][x].name == "empty":
            piece.board.move(piece, x, y)

    def king_side_castle(piece:Piece):
        ExtraFunctions.move_other(
            piece.board.get_piece(piece, 3, 0),
            -1, 0, False
        )
    def queen_side_castle(piece:Piece):
        ExtraFunctions.move_other(
            piece.board.get_piece(piece, -4, 0),
            1, 0, False
        )