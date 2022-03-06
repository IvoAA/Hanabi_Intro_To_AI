from game.game_eng import GameEngine
from dotenv import load_dotenv
import colorama

def main():
    colorama.init(autoreset=True)
    load_dotenv()
    engine = GameEngine()
    engine.start_game()


if __name__ == '__main__':
    main()
