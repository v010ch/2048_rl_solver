'''
'''

import numpy as np
import random

import constants as c

NEW_ENTRY1 = [2]
NEW_ENTRY2 = [2, 4]
NEW_ENTRY3 = [2, 4, 8]
WEIGHTS1 = [1.0]
WEIGHTS2 = [0.65, 0.35]
WEIGHTS3 = [0.65, 0.3, 0.05]


new_entry = NEW_ENTRY1
weight = WEIGHTS1


def new_game(n: int) -> np.ndarray:
    '''
    Init new game

    args:
        n: int - number of cells at row/columns

    return:
        np.ndarray - empty (zero) game state matrix
    '''
    state = np.zeros((n, n), dtype=np.uint16)  # ?uint8?

    state = add_new(state)
    state = add_new(state)

    return state


def add_new(state: np.ndarray) -> np.ndarray:
    '''
    Add one new element (2, 4, or 8) to game state matrix.
    Weights will be changed when max value becomes 4 or 8.

    args:
        mat: np.ndarray - game state matrix

    return:
        np.ndarray - game state matrix with one new value at empty space
    '''
    a = random.randint(0, state.shape[0] - 1)
    b = random.randint(0, state.shape[0] - 1)

    while state[a, b] != 0:
        a = random.randint(0, state.shape[0] - 1)
        b = random.randint(0, state.shape[0] - 1)

    element = random.choices(new_entry, weight)[0]
    state[a, b] = element

    return state


def game_state(state: np.ndarray) -> str:
    '''
    '''
    # check for win cell
    # for i in range(mat.shape[0]):
    #     for j in range(mat.shape[0]):
    #         if mat[i, j] == 2048:
    #             return 'win'
    if state.max() >= 2048:
        return 'win'

    # check for any zero entries
    # for i in range(mat.shape[0]):
    #    for j in range(mat.shape[0]):
    #        if mat[i, j] == 0:
    #            return 'not over'
    nz = np.count_nonzero(state)
    if nz != c.MAX_EL:
        return 'not over'

    # check for same cells that touch each other
    for i in range(len(state)-1):
        # intentionally reduced to check the row on the right and below
        # more elegant to use exceptions but most likely this will be their solution
        for j in range(len(state[0])-1):
            if state[i, j] == state[i+1, j] or state[i, j+1] == state[i, j]:
                return 'not over'

    for k in range(len(state)-1):  # to check the left/right entries on the last row
        if state[len(state)-1, k] == state[len(state)-1, k+1]:
            return 'not over'

    for j in range(len(state)-1):  # check up/down entries on last column
        if state[j, len(state)-1] == state[j+1, len(state)-1]:
            return 'not over'

    return 'lose'


def cover_up(state: np.ndarray):
    '''
    '''
    # new = []
    # for j in range(c.GRID_LEN):
    #     partial_new = []
    #     for i in range(c.GRID_LEN):
    #         partial_new.append(0)
    #     new.append(partial_new)
    new = np.zeros((c.GRID_LEN, c.GRID_LEN), dtype=np.uint16)

    done = False
    for i in range(c.GRID_LEN):
        count = 0
        for j in range(c.GRID_LEN):
            if state[i, j] != 0:
                new[i, count] = state[i, j]
                if j != count:
                    done = True
                count += 1

    return new, done


def merge(state: np.ndarray, done) -> tuple[np.ndarray, bool]:
    '''
    Merge cells if possible

    args:
        mat: np.ndarray - game state matrix

    return:
        Tuple:
            np.ndarray - game state matrix
            bool
    '''
    for i in range(c.GRID_LEN):
        for j in range(c.GRID_LEN-1):
            if state[i, j] == state[i, j+1] and state[i, j] != 0:
                state[i, j] *= 2
                state[i, j+1] = 0
                done = True

    return state, done


def up(state: np.ndarray) -> tuple[np.ndarray, bool]:
    '''
    Up key event handler. Shift values up and merge them if possible.

    args:
        state: np.ndarray - current game state

    return:
        np.ndarray - new game state
    '''
    # print("up")
    #game = transpose(game)
    state = np.transpose(state)
    state, done = cover_up(state)
    state, done = merge(state, done)
    state = cover_up(state)[0]
    #game = transpose(game)
    state = np.transpose(state)

    return state, done


def down(state: np.ndarray) -> tuple[np.ndarray, bool]:
    '''
    Down key event handler. Shift values down and merge them if possible.

    args:
        state: np.ndarray - current game state

    return:
        np.ndarray - new game state
    '''
    # print("down")
    #game = reverse(transpose(game))
    state = np.flip(np.transpose(state), axis=1)
    state, done = cover_up(state)
    state, done = merge(state, done)
    state = cover_up(state)[0]
    #game = transpose(reverse(game))
    state = np.transpose(np.flip(state, axis=1))

    return state, done


def left(state: np.ndarray) -> tuple[np.ndarray, bool]:
    '''
    Left key event handler. Shift values left and merge them if possible.

    args:
        state: np.ndarray - current game state

    return:
        np.ndarray - new game state
    '''
    # print("left")
    state, done = cover_up(state)
    state, done = merge(state, done)
    state = cover_up(state)[0]

    return state, done


def right(state: np.ndarray) -> tuple[np.ndarray, bool]:
    '''
    Right key event handler. Shift values right and merge them if possible.

    args:
        state: np.ndarray - current game state

    return:
        np.ndarray - new game state
    '''
    # print("right")
    #game = reverse(game)
    state = np.flip(state, axis=1)
    state, done = cover_up(state)
    state, done = merge(state, done)
    state = cover_up(state)[0]
    #game = reverse(game)
    state = np.flip(state, axis=1)

    return state, done
