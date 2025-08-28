'''
'''
from concurrent.futures import ThreadPoolExecutor
import os
import sys
import time

sys.path.insert(0, os.path.join('.', 'source'))
sys.path.insert(0, os.path.join('.', 'source', 'game'))


#from source.game.interface import GameGrid
import source.game.logic as logic
import source.game.interface as interface


if __name__ == '__main__':

    # game_grid = GameGrid()
    # game_grid.mainloop()

    logc = logic.Game2048Logic()
    interfc = interface.Game2048Interface()

    interfc.mainloop()

    with ThreadPoolExecutor(max_workers=2) as executor:
        pool1 = executor.submit(logc.run)
        time.sleep(1)
        pool2 = executor.submit(interfc.run)
