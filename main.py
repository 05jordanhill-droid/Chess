from Board import *
from ArcadeSupport import *
import arcade



def main():
    """Main function"""

    game = ArcadeSupport.setup(500, 300, "Chess", StandardBoard())
    game.run()
    


if __name__ == "__main__":
    main()