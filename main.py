from Board import *
from ArcadeSupport import *
import arcade



def main():
    game = ArcadeSupport.setup(500, 300, "Chess", StandardBoard())
    game.run()
    


if __name__ == "__main__":
    main()