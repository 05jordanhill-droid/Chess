import arcade
from Piece import Piece
from Move import Move

# These determine how far on the page the content will appear at a minimum
BASE_Y = 100
BASE_X = 220
# This is the size of the icons in the grid
INCREMENT = 16

# This is a separate support class for the purpose of making functions that are possible to easily use in the future in different programs
class ArcadeSupport:

    # Many game-like programs I have made use a grid, but since Arcade puts everything into a single list, this is an easy function to convert one to the other
    def grid_to_list(grid:list[list]):
        sprites = arcade.SpriteList()

        y = BASE_Y
        for row in grid:
            x = BASE_X
            for slot in row:
                # Some grids are very simple, housing strings rather than complex objects such as Piece
                if isinstance(slot, str):
                    sprite = arcade.Sprite(arcade.load_texture(slot))
                    sprite.center_x = x
                    sprite.center_y = y
                    sprites.append(sprite)

                elif isinstance(slot, Piece):
                    sprites.append(slot.icon)

                x += INCREMENT
            y += INCREMENT

        return sprites

    def setup(widow_width, window_height, window_title, game_setup):
        # Allowing the game to update before anything let's it process the content and put it in it's proper place to avoid any weird opening-program bugs
        game_setup.update()
        window = ArcadeGameView(widow_width, window_height, window_title, game_setup)
        window.setup()
        return window

    # Translates from a given Sprite to the underlying object variable
    def get_piece(grid:list[list], sprite:arcade.Sprite, base_width, base_height, increment):
        new_x = int((sprite.center_x - base_width) / increment)
        new_y = int((sprite.center_y - base_height) / increment)

        return grid[new_y][new_x]

    # Translates from a given Sprite to the underlying Move choice
    def get_move(sprite:arcade.Sprite, game, base_width, base_height, increment):
        new_x = int((sprite.center_x - base_width) / increment)
        new_y = int((sprite.center_y - base_height) / increment)
        
        piece:Piece = game.focus_piece

        options = []
        for move in piece.possible_moves:
            if move[0] == new_x and move[1] == new_y:
                options.append(move)

        if len(options) == 1:
            return options[0]
        else:
            print("\n\n\nCUSTOM ERROR: more than one option for move\n\n\n")


### Tutorial Disclaimer: The given class skeleton is pulled from an Arcade tutorial and populated by me ###
class ArcadeGameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, widow_width, window_height, window_title, game):
        # Call the parent class to set up the window
        super().__init__(widow_width, window_height, window_title)

        self.game = game

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        # static checkered board
        self.background_sprites = ArcadeSupport.grid_to_list(game.empty_board)
        # Moving pieces
        self.piece_sprites = ArcadeSupport.grid_to_list(game.board)
        self.move_sprites = arcade.SpriteList()
        self.message_sprites = arcade.SpriteList()

        x = BASE_X - (5 * INCREMENT)
        y = BASE_Y + (4 * INCREMENT)

        self.black_turn = arcade.Sprite("icons/black_turn.png")
        self.white_turn = arcade.Sprite("icons/white_turn.png")
        self.white_win = arcade.Sprite("icons/white_win.png")
        self.black_win = arcade.Sprite("icons/black_win.png")

        self.black_turn.center_x = x
        self.black_turn.center_y = y

        self.white_turn.center_x = x
        self.white_turn.center_y = y

        self.white_win.center_x = x
        self.white_win.center_y = y

        self.black_win.center_x = x
        self.black_win.center_y = y

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pieces = arcade.get_sprites_at_point(
            (x, y), self.piece_sprites
        )
        choices = arcade.get_sprites_at_point(
            (x, y), self.move_sprites
        )

        if choices:
            arcade.play_sound(arcade.load_sound("sounds/move.wav"))
            move = ArcadeSupport.get_move(choices[0], self.game, BASE_X, BASE_Y, INCREMENT)
            self.game.move_piece(self.game.focus_piece, move[0], move[1], move[2])

            self.move_sprites.clear()

        elif pieces:
            self.move_sprites.clear()

            piece:Piece = ArcadeSupport.get_piece(self.game.board, pieces[0], BASE_X, BASE_Y, INCREMENT)

            if piece.direction == piece.board.turn:
                self.game.update()

                moves:list[Move] = piece.possible_moves

                self.game.focus_piece = piece
                self.game.focus_moves = moves

                for move in moves:
                    option = arcade.Sprite(arcade.load_texture("icons/option.png"))
                    option.center_x = (move[0] * INCREMENT) + BASE_X
                    option.center_y = (move[1] * INCREMENT) + BASE_Y
                    self.move_sprites.append(option)



    def on_draw(self):
        """Render the screen."""

        # The clear method should always be called at the start of on_draw.
        # It clears the whole screen to whatever the background color is
        # set to. This ensures that you have a clean slate for drawing each
        # frame of the game.
        self.clear()

        self.message_sprites.clear()

        if self.game.turn == 1:
            self.message_sprites.append(self.black_turn)
        elif self.game.turn == -1:
            self.message_sprites.append(self.white_turn)

        for team in self.game.teams:
            choices = []
            king_captured = True
            for piece in team.team:
                if piece.crucial:
                    king_captured = False
                for move in piece.possible_moves:
                    choices.append(move)

            if choices == [] or king_captured:
                self.message_sprites.clear()
                if piece.direction == 1:
                    self.message_sprites.append(self.white_win)
                elif piece.direction == -1:
                    self.message_sprites.append(self.black_win)

        

        # Code to draw other things will go here
        self.background_sprites.draw()
        self.piece_sprites.draw()
        self.move_sprites.draw()
        self.message_sprites.draw()