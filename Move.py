from Conditions import *

class Move:
    def __init__(self, x_offset:int=0, y_offset:int=0, continuous:bool=False, jump:bool=False, increment:int=1, conditions:list=[], extra_functions:list=[], direction:int=1, special=False):
        # bishop, rook, queen
        self.continuous = continuous
        # knight
        self.jump = jump
        # castling, pawn capturing, pawn movement
        self.conditions = conditions

        self.x_offset = x_offset * direction
        self.y_offset = y_offset * direction

        self.increment = increment
        self.extra_functions = extra_functions
        self.direction = direction

        # Special Moves are skipped in certain cases to prevent circular processing
        self.special = special

    # This is always run with the Move, but the extra_functions can be empty as desired
    def run(self, piece):
        for extra_function in self.extra_functions:
            extra_function()



class KingSideCastle(Move):
    def __init__(self, piece):
        super().__init__(3, 0, False, False, 1, [Conditions.king_side_castle], [
            lambda: ExtraFunctions.king_side_castle(piece)
        ], special=True)

class QueenSideCastle(Move):
    def __init__(self, piece):
        super().__init__(-4, 0, False, False, 1, [Conditions.queen_side_castle], [
            lambda: ExtraFunctions.queen_side_castle(piece)
        ], special=True)