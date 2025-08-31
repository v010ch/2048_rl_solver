'''
'''

import random
import socket
import time
from typing import Optional

import numpy as np

import constants as c

NEW_VALS = [2, 4, 8]
WEIGHTS2 = [1.0, 0.0, 0.0]
WEIGHTS4 = [0.65, 0.35, 0.0]
WEIGHTS8 = [0.65, 0.3, 0.05]


class Game2048Logic():
    def __init__(self, size: Optional[int] = c.GRID_LEN):
        self.__weights = WEIGHTS2
        self.__cur_max = 2

        if size > 5 or size < 3:
            raise ValueError(f'Wrong matrix size {size}.\nShould be >2 and <6.')
        self.__size = size
        self.__state = np.zeros((self.__size), dtype=np.uint16)
        self.__exit = False
        #self.server = socket.socket()
        # self.server.bind((ADDR, PORT))
        pass

    def run(self):
        print('run logic')
        #self.server.bind(('localhost', 8089))
        #self.server.listen(50)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print('1')
            s.bind((c.ADDR, c.PORT))
            print('server logic await connection')
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
        new = np.zeros((self.__size, self.__size), dtype=np.uint16)

        done = False
        for i in range(self.__size):
            count = 0
            for j in range(self.__size):
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
        for i in range(self.__size):
            for j in range(self.__size-1):
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
