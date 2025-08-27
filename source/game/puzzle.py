'''
'''
import random

from tkinter import Frame, Label, CENTER

from . import logic
from . import constants as c


class GameGrid(Frame):
    '''
    '''
    def __init__(self):
        Frame.__init__(self)

        self.GRID_SIZE = c.GRID_LEN
        self.grid()
        self.master.title('2048')
        # self.master.bind("<Key>", self.key_down)
        self.master.bind("<KeyRelease>", self.key_up)

        # set up methoda for key release event handler
        self.commands = {
            c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right,
            c.KEY_UP_ALT1: logic.up,
            c.KEY_DOWN_ALT1: logic.down,
            c.KEY_LEFT_ALT1: logic.left,
            c.KEY_RIGHT_ALT1: logic.right,
        }

        self.grid_cells = []
        self.init_grid()
        self.state = logic.new_game(self.GRID_SIZE)
        self.history_matrixs = []
        self.update_grid_cells()

        # self.mainloop()

    def init_grid(self) -> None:
        '''
        '''
        background = Frame(self, bg=c.BG_COLOR_GAME,
                           width=c.SIZE, height=c.SIZE,
                           )
        background.grid()

        for i in range(self.GRID_SIZE):
            grid_row = []
            for j in range(self.GRID_SIZE):
                cell = Frame(
                    background,
                    bg=c.BG_COLOR_CELL_EMPTY,
                    width=c.SIZE / self.GRID_SIZE,
                    height=c.SIZE / self.GRID_SIZE
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

    def update_grid_cells(self) -> None:
        '''
        '''
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                new_number = self.state[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=c.BG_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=c.BG_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number]
                    )
        self.update_idletasks()

    def key_up(self, event) -> None:
        '''
        '''
        key = event.keysym
        print(event)
        if key == c.KEY_QUIT:
            exit()

        if key == c.KEY_BACK and len(self.history_matrixs) > 1:
            self.state = self.history_matrixs.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))
        elif key in self.commands:
            self.state, done = self.commands[key](self.state)
            if done:
                self.state = logic.add_new(self.state)
                # record last move
                self.history_matrixs.append(self.state)
                self.update_grid_cells()
                if logic.game_state(self.state) == 'win':
                    self.grid_cells[1][1].configure(text="You", bg=c.BG_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!", bg=c.BG_COLOR_CELL_EMPTY)
                if logic.game_state(self.state) == 'lose':
                    self.grid_cells[1][1].configure(text="You", bg=c.BG_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!", bg=c.BG_COLOR_CELL_EMPTY)
