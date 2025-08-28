'''
'''

import random
import socket
import time

import numpy as np

import constants as c

NEW_VALS = [2, 4, 8]
WEIGHTS2 = [1.0, 0.0, 0.0]
WEIGHTS4 = [0.65, 0.35, 0.0]
WEIGHTS8 = [0.65, 0.3, 0.05]


class Game2048Logic():
    def __init__(self):
        self.__weights = WEIGHTS2
        self.__cur_max = 2
        self.__state = np.zeros((c.GRID_LEN), dtype=np.uint16)
        self.__exit = False
        #self.server = socket.socket()
        # self.server.bind((ADDR, PORT))
        pass

    def run(self):
        #self.server.bind(('localhost', 8089))
        #self.server.listen(50)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 19089))
            s.listen(50)
            conn, addr = s.accept()
            print(f'Connection established with {addr}')

            for idx in range(50):
                print(f'{idx:02d}: this is logic')
                time.sleep(0.5)

            while not self.__exit:
                # send state
                # get comand
                # calculate new state
                self.__exit = True

    def new_game(self, n: int) -> np.ndarray:
        '''
        Init new game

        args:
            n: int - number of cells at row/columns

        return:
            np.ndarray - empty (zero) game state matrix
        '''
        self.__weights = WEIGHTS2
        self.__cur_max = 2

        state = np.zeros((n, n), dtype=np.uint16)  # ?uint8?

        state = self.add_new(state)
        state = self.add_new(state)

        return state

    def add_new(self, state: np.ndarray) -> np.ndarray:
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

        element = random.choices(NEW_VALS, self.__weights)[0]
        state[a, b] = element

        return state


    def cover_up(self, state: np.ndarray):
        '''
        '''
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


    def merge(self, state: np.ndarray, done) -> tuple[np.ndarray, bool]:
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


    def up(self, state: np.ndarray) -> tuple[np.ndarray, bool]:
        '''
        Up key event handler. Shift values up and merge them if possible.

        args:
            state: np.ndarray - current game state

        return:
            np.ndarray - new game state
        '''
        # print("up")
        state = np.transpose(state)
        state, done = self.cover_up(state)
        state, done = self.merge(state, done)
        state = self.cover_up(state)[0]
        state = np.transpose(state)

        return state, done


    def down(self, state: np.ndarray) -> tuple[np.ndarray, bool]:
        '''
        Down key event handler. Shift values down and merge them if possible.

        args:
            state: np.ndarray - current game state

        return:
            np.ndarray - new game state
        '''
        # print("down")
        state = np.flip(np.transpose(state), axis=1)
        state, done = self.cover_up(state)
        state, done = self.merge(state, done)
        state = self.cover_up(state)[0]
        state = np.transpose(np.flip(state, axis=1))

        return state, done


    def left(self, state: np.ndarray) -> tuple[np.ndarray, bool]:
        '''
        Left key event handler. Shift values left and merge them if possible.

        args:
            state: np.ndarray - current game state

        return:
            np.ndarray - new game state
        '''
        # print("left")
        state, done = self.cover_up(state)
        state, done = self.merge(state, done)
        state = self.cover_up(state)[0]

        return state, done


    def right(self, state: np.ndarray) -> tuple[np.ndarray, bool]:
        '''
        Right key event handler. Shift values right and merge them if possible.

        args:
            state: np.ndarray - current game state

        return:
            np.ndarray - new game state
        '''
        # print("right")
        state = np.flip(state, axis=1)
        state, done = self.cover_up(state)
        state, done = self.merge(state, done)
        state = self.cover_up(state)[0]
        state = np.flip(state, axis=1)

        return state, done













def new_game_old(n: int) -> np.ndarray:
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


def add_new_old(state: np.ndarray) -> np.ndarray:
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


def game_state_old(state: np.ndarray) -> str:
    '''
    '''
    if state.max() >= 2048:
        return 'win'

    nz = np.count_nonzero(state)
    if nz != c.MAX_EL:
        return 'not over'

    # check for same cells that touch each other
    for i in range(state.shape[0]-1):
        # intentionally reduced to check the row on the right and below
        # more elegant to use exceptions but most likely this will be their solution
        for j in range(state.shape[0]-1):
            if state[i, j] == state[i+1, j] or state[i, j+1] == state[i, j]:
                return 'not over'

    for k in range(state.shape[0]-1):  # to check the left/right entries on the last row
        if state[state.shape[0]-1, k] == state[state.shape[0]-1, k+1]:
            return 'not over'

    for j in range(state.shape[0]-1):  # check up/down entries on last column
        if state[j, state.shape[0]-1] == state[j+1, state.shape[0]-1]:
            return 'not over'

    return 'lose'


def cover_up_old(state: np.ndarray):
    '''
    '''
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


def merge_old(state: np.ndarray, done) -> tuple[np.ndarray, bool]:
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


def up_old(state: np.ndarray) -> tuple[np.ndarray, bool]:
    '''
    Up key event handler. Shift values up and merge them if possible.

    args:
        state: np.ndarray - current game state

    return:
        np.ndarray - new game state
    '''
    # print("up")
    state = np.transpose(state)
    state, done = cover_up(state)
    state, done = merge(state, done)
    state = cover_up(state)[0]
    state = np.transpose(state)

    return state, done


def down_old(state: np.ndarray) -> tuple[np.ndarray, bool]:
    '''
    Down key event handler. Shift values down and merge them if possible.

    args:
        state: np.ndarray - current game state

    return:
        np.ndarray - new game state
    '''
    # print("down")
    state = np.flip(np.transpose(state), axis=1)
    state, done = cover_up(state)
    state, done = merge(state, done)
    state = cover_up(state)[0]
    state = np.transpose(np.flip(state, axis=1))

    return state, done


def left_old(state: np.ndarray) -> tuple[np.ndarray, bool]:
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


def right_old(state: np.ndarray) -> tuple[np.ndarray, bool]:
    '''
    Right key event handler. Shift values right and merge them if possible.

    args:
        state: np.ndarray - current game state

    return:
        np.ndarray - new game state
    '''
    # print("right")
    state = np.flip(state, axis=1)
    state, done = cover_up(state)
    state, done = merge(state, done)
    state = cover_up(state)[0]
    state = np.flip(state, axis=1)

    return state, done
