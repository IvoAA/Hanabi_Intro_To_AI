import concurrent.futures
from utils.screen import enable_print, block_print
from main import run_game
from concurrent.futures import ThreadPoolExecutor
import time
import multiprocessing

"""
Keep the batch size small in case of having a slow computer.
This runner will execute batches times batch_size games and return the average point and number of plays for a given agent.
"""
batches: int = 10
batch_size: int = 10
total_games = batches * batch_size

def run_process():
    print(f"Starting {total_games} games. Might take a while (around 1min/50games).")
    block_print()
    start_time = time.time()
    total_score = 0
    total_plays = 0
    q = multiprocessing.Queue()
    for batch in range(batches):
        print(f"Starting batch {batch}")
        current_batch = []
        for _ in range(batch_size):
            p = multiprocessing.Process(target=run_game, args=(q,))
            current_batch.append(p)

        for p in current_batch:
            p.start()
        for p in current_batch:
            p.join()

    q.put('STOP')
    l = dump_queue(q)
    for measure in l:
        total_score += measure[0]
        total_plays += measure[1]

    enable_print()
    print("--- %s seconds ---" % (time.time() - start_time))
    print(
        f"Played {total_games} games with an average score of {total_score / total_games} and average number of plays "
        f"of {total_plays / total_games}")



def run_multiple_games():
    print(f"Starting {total_games} games. Might take a while (around 1min/10games).")
    block_print()
    start_time = time.time()
    total_score = 0
    total_plays = 0
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for _ in range(total_games):
            futures.append(executor.submit(run_game))
        for future in concurrent.futures.as_completed(futures):
            score, plays = future.result()
            total_score += score
            total_plays += plays
    enable_print()
    print("--- %s seconds ---" % (time.time() - start_time))
    print(
        f"Played {total_games} games with an average score of {total_score / total_games} and average number of plays "
        f"of {total_plays / total_games}")


def dump_queue(queue):
    """
    https://stackoverflow.com/questions/1540822/dumping-a-multiprocessing-queue-into-a-list
    Empties all pending items in a queue and returns them in a list.
    """
    result = []

    for i in iter(queue.get, 'STOP'):
        result.append(i)
    time.sleep(.1)
    return result

if __name__ == '__main__':
    run_process()
