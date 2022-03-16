import time

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

def run_game(q=None):
    start_time = time.time()
    colorama.init(autoreset=True)
    load_dotenv()
    engine = GameEngine()
    engine.start_game()
    score = engine.game_board.card_board.score()
    print("--- %s seconds ---" % (time.time() - start_time))
    print(f"Game over score - {score}, actions {engine.game_board.nr_actions}")
    if q:
        q.put((score, engine.game_board.nr_actions, engine.game_board.finish_reason))
    return score, engine.game_board.nr_actions


if __name__ == '__main__':
    run_game()
