from Conditions import *

class Move:
    def __init__(self, x_offset:int=0, y_offset:int=0, continuous:bool=False, jump:bool=False, increment:int=1, conditions:list=[], extra_functions:list=[], direction:int=1, special=False):
        self.continuous = continuous
        self.jump = jump
        self.conditions = conditions
        self.x_offset = x_offset * direction
        self.y_offset = y_offset * direction
        self.increment = increment
        self.extra_functions = extra_functions
        self.direction = direction
        self.special = special

    def run(self, piece):
        for extra_function in self.extra_functions:
            extra_function()


    def add_x_offset(self, x_offset:int):
        self.x_offset = x_offset


    def add_y_offset(self, y_offset:int):
        self.y_offset = y_offset


    def make_continuous(self, set_true:bool=True, increment:int=1):
        if set_true:
            self.continuous = True
            self.increment = increment
        else:
            self.continuous = False


    def let_jump(self, set_true:bool=True):
        if set_true:
            self.jump = True
        else:
            self.jump = False


    def add_condition(self, condition):
        self.conditions.append(condition)

    def add_extra_function(self, extra_function):
        self.extra_functions.append(extra_function)



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