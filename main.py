from game.game_eng import GameEngine
from dotenv import load_dotenv
import colorama
import logging, sys
import random


log = logging.getLogger(__name__)

# noinspection PyArgumentList
logging.basicConfig(format="{filename}:{lineno} {asctime} {levelname[0]} - {message}",
                    datefmt="%H:%M:%S",
                    level=logging.INFO,
                    stream=sys.stdout,
                    style='{')


def main():
    random.seed(1337)
    colorama.init(autoreset=True)
    load_dotenv()
    engine = GameEngine()
    engine.start_game()


if __name__ == '__main__':
    main()
