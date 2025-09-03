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
import source.solver.solver as solver


if __name__ == '__main__':

    print('starting')

    logc = logic.Game2048Logic()

    args = sys.argv[1:]
    print(args)

    used_class = interface.Game2048Interface

    if 'solver' in args:
        used_class = solver.SolverClass

    with ThreadPoolExecutor(max_workers=2) as executor:
        pool1 = executor.submit(logc.run)
        time.sleep(1)
        #$interfc = interface.Game2048Interface()
        #pool2 = executor.submit(interfc.mainloop())

        client = used_class()
        pool2 = executor.submit(client.mainloop())
