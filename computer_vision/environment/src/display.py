'''Display environment'''
import pygame as pg
import numpy as np
try:
    from board import Board
    from lib import Objects
except ImportError:
    from .board import Board
    from .lib import Objects

class DisplayEnvironment:
    '''Displaying the environment with pygame'''
    def __init__(self, window_size: tuple(int, int), board_size: tuple(int, int), caption: str=''):
        self.window_size = window_size
        self.board_size = board_size

        pg.init()
        # Init game window
        pg.display.set_caption(caption)
        self.display_window = pg.display.set_mode(window_size)

        self.fps = pg.time.Clock()

        square_size = self.window_size[1] / self.board_size[0]
        self.board = Board((self.board_size[1], self.board_size[0]), square_size)

    def display(self):
        '''
        Display the matrix
        '''
        # Draw the grid on the screen
        self.board.draw(self.display_window)

    def update(self, board: np.dnarray):
        '''Update the display'''
        self.board.reset(board)
        pg.display.update()

    def insert(self, pos, name):
        '''Insert an object into the map'''
        object_data = Objects().get_data(name)
        self.board.insert(pos, object_data.id)
