'''
'''
from concurrent.futures import ThreadPoolExecutor
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join('.', 'source'))
sys.path.insert(0, os.path.join('.', 'source', 'game'))


#from source.game.interface import GameGrid
import source.game.logic as logic
import source.game.interface as interface
import source.solver.solver as solver


if __name__ == '__main__':

    print('starting')

    args = sys.argv[1:]
    print(args)

    if '-solver' in args:
        used_class = solver.SolverClass

    test_state = None
    if '-test' in args:
        with open('test.txt', 'r') as fd:
            test_state = fd.read().split()
            size = int(test_state[0])
            test_state = np.array([int(el) for el in test_state[1:]])\
                           .reshape((size, size))

    #logc = logic.Game2048Logic(state=test_state)
    logc = logic.Game2048Logic()
    used_class = interface.Game2048Interface

    with ThreadPoolExecutor(max_workers=2) as executor:
        pool1 = executor.submit(logc.run)
        time.sleep(1)
        #$interfc = interface.Game2048Interface()
        #pool2 = executor.submit(interfc.mainloop())

        client = used_class()
        pool2 = executor.submit(client.mainloop())
