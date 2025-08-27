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
    return:
        np.ndarray - 
    '''
    matrix = np.zeros((n, n), dtype=np.uint16)  # ?uint8?

    matrix = add_new(matrix)
    matrix = add_new(matrix)

    return matrix


def add_new(mat: np.ndarray) -> np.ndarray:
    '''
    '''
    a = random.randint(0, mat.shape[0] - 1)
    b = random.randint(0, mat.shape[0] - 1)

    while mat[a, b] != 0:
        a = random.randint(0, mat.shape[0] - 1)
        b = random.randint(0, mat.shape[0] - 1)

    element = random.choices(new_entry, weight)[0]
    mat[a, b] = element

    return mat


def game_state(mat: np.ndarray) -> str:
    '''
    '''
    # check for win cell
    # for i in range(mat.shape[0]):
    #     for j in range(mat.shape[0]):
    #         if mat[i, j] == 2048:
    #             return 'win'
    if mat.max() >= 2048:
        return 'win'

    # check for any zero entries
    # for i in range(mat.shape[0]):
    #    for j in range(mat.shape[0]):
    #        if mat[i, j] == 0:
    #            return 'not over'
    nz = np.count_nonzero(mat)
    if nz != c.MAX_EL:
        return 'not over'

    # check for same cells that touch each other
    for i in range(len(mat)-1):
        # intentionally reduced to check the row on the right and below
        # more elegant to use exceptions but most likely this will be their solution
        for j in range(len(mat[0])-1):
            if mat[i, j] == mat[i+1, j] or mat[i, j+1] == mat[i, j]:
                return 'not over'

    for k in range(len(mat)-1):  # to check the left/right entries on the last row
        if mat[len(mat)-1, k] == mat[len(mat)-1, k+1]:
            return 'not over'

    for j in range(len(mat)-1):  # check up/down entries on last column
        if mat[j, len(mat)-1] == mat[j+1, len(mat)-1]:
            return 'not over'

    return 'lose'


def reverse_old(mat: np.ndarray) -> np.ndarray:
    '''
    '''
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0])-j-1])

    return new


def transpose_old(mat: np.ndarray) -> np.ndarray:
    '''
    '''
    new = []
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])

    return new


def cover_up(mat: np.ndarray):
    '''
    '''
    # new = []
    # for j in range(c.GRID_LEN):
    #     partial_new = []
    #     for i in range(c.GRID_LEN):
    #         partial_new.append(0)
    #     new.append(partial_new)
    new = np.zeros((4, 4), dtype=np.uint16)

    done = False
    for i in range(c.GRID_LEN):
        count = 0
        for j in range(c.GRID_LEN):
            if mat[i, j] != 0:
                new[i, count] = mat[i, j]
                if j != count:
                    done = True
                count += 1

    return new, done


def merge(mat: np.ndarray, done):
    '''
    '''
    for i in range(c.GRID_LEN):
        for j in range(c.GRID_LEN-1):
            if mat[i, j] == mat[i, j+1] and mat[i, j] != 0:
                mat[i, j] *= 2
                mat[i, j+1] = 0
                done = True

    return mat, done


def up(game):
    '''
    '''
    print("up")
    # return matrix after shifting up
    #game = transpose(game)
    game = np.transpose(game)
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    #game = transpose(game)
    game = np.transpose(game)

    return game, done


def down(game):
    '''
    '''
    print("down")
    # return matrix after shifting down
    #game = reverse(transpose(game))
    game = np.flip(np.transpose(game), axis=1)
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    #game = transpose(reverse(game))
    game = np.transpose(np.flip(game, axis=1))

    return game, done


def left(game):
    '''
    '''
    print("left")
    # return matrix after shifting left
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]

    return game, done


def right(game):
    '''
    '''
    print("right")
    # return matrix after shifting right
    #game = reverse(game)
    game = np.flip(game, axis=1)
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    #game = reverse(game)
    game = np.flip(game, axis=1)

    return game, done
