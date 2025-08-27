'''
'''

import os
import sys

sys.path.insert(0, os.path.join('.', 'source'))
sys.path.insert(0, os.path.join('.', 'source', 'game'))


from source.game.puzzle import GameGrid


if __name__ == '__main__':

    game_grid = GameGrid()
    game_grid.mainloop()
