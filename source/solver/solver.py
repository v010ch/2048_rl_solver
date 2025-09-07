'''
'''
import random
import socket


import numpy as np
from torch import nn

ADDR = '127.0.0.1'
PORT = 9093
CMD_LEN = 5
STATE_PACK_SIZE = {3: 18, 4: 32, 5: 50}
DIRECTIONS = {0: 'up___',
              1: 'down_',
              2: 'left_',
              3: 'right',
              }


class SolverClass(nn.Module):
    '''
    '''
    def __init__(self,):
        super().__init__()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((ADDR, PORT))
        self.__GRID_SIZE = int(self.__socket.recv(1)
                                            .decode()
                               )
        self.__state = np.zeros((self.__GRID_SIZE, self.__GRID_SIZE),
                                dtype=np.int16)

        self.__exit = False


    def forward(self, state: np.ndarray) -> np.ndarray:
        '''
        '''
        print('forward')
        return np.array([0.25, 0.25, 0.25, 0.25])


    def train(self):
        '''
        '''
        pass


    def make_move(self, state: np.ndarray) -> str:
        '''
        '''
        print('in make move')
        vals = self.forward(state)
        print(vals)
        # return DIRECTIONS[vals.argmax()]
        return random.choices(list(DIRECTIONS.values()), vals)


    def run(self):
        '''
        '''
        # get game state

        # loop
        # calculate move
        move = self.make_move(self.__state)
        # send command
        self.__socket.send(move.encode())
        # get game state
        self.__state = self.__get_state()
        # calculate reward
        rwrd = self.__calculate_reward(self.__state)


    def __get_state(self) -> np.ndarray:
        '''
        '''
        tmp = self.__socket.recv(STATE_PACK_SIZE[self.__GRID_SIZE])
        tmp = np.frombuffer(tmp, dtype=np.uint16)\
                .reshape((self.__GRID_SIZE, self.__GRID_SIZE))
        # decode from string
        return tmp


    def __calculate_reward(self, state: np.ndarray) -> int:
        '''
        '''
        return 0


    def mainloop(self):
        '''
        '''
        print('solver mainloop')

        epoch = 2
        state = self.__get_state()

        # for idx in range(50):
        #     print(f'{idx:02d}: this is logic')
        #     time.sleep(0.5)

        while not self.__exit:
            # send comand
            command = 'new__'
            for idx in range(epoch):
                print(f'Epoch: {idx}')

                self.__socket.send(command.encode())
                print('command send')
                state = self.__get_state()
                print(f'getting state: {state}')
                command = self.make_move(state)
                print(f'make move {command}')


            self.__exit = True

            # calculate new state
            #done = self.__execute_command(command.decode())
            #if done:
            #    self.__state = self.__add_new(self.__state)
            #self.__send_state()
            # self.__exit = True

        self.__socket.send('exit_'.encode())
        print('solver: end of the main loop')
