'''
'''
import random
import socket
import time

import numpy as np
from tkinter import Frame, Label, CENTER

from . import logic
from . import constants as c



class Game2048Interface(Frame):
    '''
    '''
    def __init__(self):
        Frame.__init__(self)

        # establishing connection with server
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((c.ADDR, c.PORT))
        self.__GRID_SIZE = int(self.__socket.recv(1)
                                            .decode()
                               )
        # self.__GRID_SIZE = c.GRID_LEN

        self.__command = 'idle'
        self.grid()
        self.master.title('2048')
        # self.master.bind("<Key>", self.key_down)
        self.master.bind("<KeyRelease>", self.key_up)
        self.__state = np.zeros((self.__GRID_SIZE, self.__GRID_SIZE))
        # self.history_matrixs = []

        # set up methoda for key release event handler
        self.commands = {
            c.KEY_UP: self.__up,
            c.KEY_DOWN: self.__down,
            c.KEY_LEFT: self.__left,
            c.KEY_RIGHT: self.__right,
            c.KEY_UP_ALT1: self.__up,
            c.KEY_DOWN_ALT1: self.__down,
            c.KEY_LEFT_ALT1: self.__left,
            c.KEY_RIGHT_ALT1: self.__right,

            c.KEY_QUIT: self.__exit,
        }

        self.grid_cells = []
        self.init_grid()

        self.__state = self.__get_new_state()
        self.__update_grid_cells()
        print(self.__state)


    def __del__(self):
        self.__socket.close()


    def init_grid(self) -> None:
        '''
        '''
        background = Frame(self, bg=c.BG_COLOR_GAME,
                           width=c.SIZE, height=c.SIZE, ## new sizes with new grid size
                           )
        background.grid()

        for i in range(self.__GRID_SIZE):
            grid_row = []
            for j in range(self.__GRID_SIZE):
                cell = Frame(
                    background,
                    bg=c.BG_COLOR_CELL_EMPTY,
                    width=c.SIZE / self.__GRID_SIZE,
                    height=c.SIZE / self.__GRID_SIZE
                )
                cell.grid(
                    row=i,
                    column=j,
                    padx=c.GRID_PADDING,
                    pady=c.GRID_PADDING
                )
                t = Label(
                    master=cell,
                    text="",
                    bg=c.BG_COLOR_CELL_EMPTY,
                    justify=CENTER,
                    font=c.FONT,
                    width=5,
                    height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)


    def __update_grid_cells(self) -> None:
        '''
        Update grid cells of interface with current values.
        '''
        for i in range(self.__GRID_SIZE):
            for j in range(self.__GRID_SIZE):
                new_number = self.__state[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=c.BG_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=c.BG_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number]
                    )
        self.update_idletasks()


    def __send_command(self, ) -> None:
        '''
        Send command to server (logic)
        '''
        self.__socket.send(self.__command.encode())


    def __get_new_state(self, ) -> np.ndarray:
        '''
        Get new game state from server (logic)

        return:
            np.ndarray - new game state
        '''
        print(f'getting {c.STATE_PACK_SIZE[self.__GRID_SIZE]}')
        tmp = self.__socket.recv(c.STATE_PACK_SIZE[self.__GRID_SIZE])
        tmp = np.frombuffer(tmp, dtype=np.uint16)\
                .reshape((self.__GRID_SIZE, self.__GRID_SIZE))

        return tmp


    def key_up(self, event) -> None:
        '''
        Handler for key_up events.
        '''
        key = event.keysym
        print(event)
        if key == c.KEY_QUIT:
            self.__state = self.commands[key]()
            exit()

        # if key == c.KEY_BACK and len(self.history_matrixs) > 1:
        #    self.state = self.history_matrixs.pop()
        #    self.__update_grid_cells()
        #    print('back on step total step:', len(self.history_matrixs))
        # el
        if key in self.commands:
            # self.__state, done = self.commands[key]()
            self.__state = self.commands[key]()
            self.__update_grid_cells()

            # if done:
            if False:
                # record last move
                # self.history_matrixs.append(self.state)
                self.__update_grid_cells()
                if logic.game_state(self.__state) == 'win':
                    self.grid_cells[1][1].configure(text="You", bg=c.BG_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!", bg=c.BG_COLOR_CELL_EMPTY)
                if logic.game_state(self.__state) == 'lose':
                    self.grid_cells[1][1].configure(text="You", bg=c.BG_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!", bg=c.BG_COLOR_CELL_EMPTY)


    def __up(self) -> np.ndarray:
        '''
        Up key event handler. Shift values up and merge them if possible.

        return:
            np.ndarray - new game state
        '''
        # print("up")
        self.__command = 'up___'
        self.__send_command()
        state = self.__get_new_state()

        return state


    def __down(self) -> np.ndarray:
        '''
        Down key event handler. Shift values down and merge them if possible.

        return:
            np.ndarray - new game state
        '''
        # print("down")
        self.__command = 'down_'
        self.__send_command()
        state = self.__get_new_state()

        return state


    def __left(self) -> np.ndarray:
        '''
        Left key event handler. Shift values left and merge them if possible.

        return:
            np.ndarray - new game state
        '''
        # print("left")
        self.__command = 'left_'
        self.__send_command()
        state = self.__get_new_state()

        return state


    def __right(self) -> np.ndarray:
        '''
        Right key event handler. Shift values right and merge them if possible.

        return:
            np.ndarray - new game state
        '''
        # print("right")
        self.__command = 'right'
        self.__send_command()
        state = self.__get_new_state()

        return state


    def __exit(self) -> np.ndarray:
        '''
        Escape key event handler. End of the program.
        '''
        self.__command = 'exit_'
        self.__send_command()

        return np.zeros_like(self.__state)
