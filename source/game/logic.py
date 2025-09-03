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
        self.__conn = None

        if size > 5 or size < 3:
            raise ValueError(f'Wrong size {size}.\nShould be 3 < and < 5.')

        self.__grid_size = size

        # create new game
        self.__state = np.zeros((self.__grid_size, self.__grid_size),
                                dtype=np.uint16
                                )
        self.__state = self.__new_game(self.__grid_size)

        # command to exit main loop
        self.__exit = False


    def run(self):
        '''
        Logic (server) main loop
        '''
        print('run logic')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((c.ADDR, c.PORT))
            print('server logic await connection')
            s.listen(50)
            self.__conn, addr = s.accept()
            print(f'Connection established with {addr}')

            # send grid size and init state to interface
            self.__conn.send(str(self.__grid_size).encode())
            self.__send_state()

            # for idx in range(50):
            #     print(f'{idx:02d}: this is logic')
            #     time.sleep(0.5)

            while not self.__exit:
                # get comand
                command = self.__conn.recv(c.CMD_LEN)
                # calculate new state
                done = self.__execute_command(command.decode())
                if done:
                    self.__state = self.__add_new(self.__state)
                self.__send_state()
                # self.__exit = True
            print('logic: end of the main loop')


    def __send_state(self) -> None:
        '''
        Send state to consumer (interface/solver)
        '''
        # print(self.__state)
        tmp = self.__state.tostring()
        # print(f'sending {len(tmp)}')
        self.__conn.send(tmp)


    def __execute_command(self, cmd: str) -> None:
        '''
        Execute recived command.
        '''
        print(cmd)
        if cmd == 'up___':
            self.__state, done = self.__up(self.__state)
            return done

        if cmd == 'down_':
            self.__state, done = self.__down(self.__state)
            return done

        if cmd == 'left_':
            self.__state, done = self.__left(self.__state)
            return done

        if cmd == 'right':
            self.__state, done = self.__right(self.__state)
            return done

        # if return True - one more new element will иу added
        if cmd == 'new__':
            self.__state = self.__new_game(self.__grid_size)
            return False

        if cmd == 'exit_':
            self.__exit = True
            return False

        return False


    def __new_game(self, n: int) -> np.ndarray:
        '''
        Init new game

        args:
            n: int - number of cells at row/columns

        return:
            np.ndarray - new game state matrix with only two init values
        '''
        self.__weights = WEIGHTS2
        self.__cur_max = 2

        state = np.zeros((n, n), dtype=np.uint16)  # ?uint8?

        state = self.__add_new(state)
        state = self.__add_new(state)

        return state


    def __add_new(self, state: np.ndarray) -> np.ndarray:
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

        element = random.choices(NEW_VALS, self.__weights, k=1)[0]
        state[a, b] = element

        return state


    def __cover_up(self, state: np.ndarray):
        '''
        '''
        new = np.zeros_like(state)
        done = False

        for i in range(self.__grid_size):
            count = 0
            for j in range(self.__grid_size):
                if state[i, j] != 0:
                    new[i, count] = state[i, j]
                    if j != count:
                        done = True
                    count += 1

        return new, done


    def __merge(self, state: np.ndarray) -> tuple[np.ndarray, bool]:
        '''
        Merge cells if possible - return state and True.
        If no cels was merged - return state and False.

        args:
            mat: np.ndarray - game state matrix

        return:
            Tuple:
                np.ndarray - game state matrix
                bool - True if at least one merge (game not end)
        '''
        done = False
        for i in range(self.__grid_size):
            for j in range(self.__grid_size - 1):
                if state[i, j] == state[i, j + 1] and state[i, j] != 0:
                    state[i, j] *= 2
                    state[i, j+1] = 0
                    done = True

        return state, done


    def __up(self, state: np.ndarray) -> tuple[np.ndarray, bool]:
        '''
        Up key event handler. Shift values up and merge them if possible.

        args:
            state: np.ndarray - current game state

        return:
            np.ndarray - new game state
            bool - True - if game not ended
        '''
        # print('logic: up')
        state = np.transpose(state)
        state, done_c = self.__cover_up(state)
        state, done_m = self.__merge(state)
        state = self.__cover_up(state)[0]
        state = np.transpose(state)

        # return state, (done_c and done_m)
        return state, (done_c or done_m)


    def __down(self, state: np.ndarray) -> tuple[np.ndarray, bool]:
        '''
        Down key event handler. Shift values down and merge them if possible.

        args:
            state: np.ndarray - current game state

        return:
            np.ndarray - new game state
            bool - True - if game not ended
        '''
        # print('logic: down')
        state = np.flip(np.transpose(state), axis=1)
        state, done_c = self.__cover_up(state)
        state, done_m = self.__merge(state)
        state = self.__cover_up(state)[0]
        state = np.transpose(np.flip(state, axis=1))

        # return state, (done_c and done_m)
        return state, (done_c or done_m)


    def __left(self, state: np.ndarray) -> tuple[np.ndarray, bool]:
        '''
        Left key event handler. Shift values left and merge them if possible.

        args:
            state: np.ndarray - current game state

        return:
            np.ndarray - new game state
            bool - True - if game not ended
        '''
        # print('logic: left')
        state, done_c = self.__cover_up(state)
        state, done_m = self.__merge(state)
        state = self.__cover_up(state)[0]

        # return state, (done_c and done_m)
        return state, (done_c or done_m)


    def __right(self, state: np.ndarray) -> tuple[np.ndarray, bool]:
        '''
        Right key event handler. Shift values right and merge them if possible.

        args:
            state: np.ndarray - current game state

        return:
            np.ndarray - new game state
            bool - True - if game not ended
        '''
        # print('logic: right')
        state = np.flip(state, axis=1)
        state, done_c = self.__cover_up(state)
        state, done_m = self.__merge(state)
        state = self.__cover_up(state)[0]
        state = np.flip(state, axis=1)

        # return state, (done_c and done_m)
        return state, (done_c or done_m)
