'''Display environment'''
import pygame as pg
from .board import Board
from .lib import Objects

class DisplayEnvironment:
    '''Displaying the environment with pygame'''
    def __init__(self, window_size, board_size, caption=''):
        self.window_size = window_size
        self.board_size = board_size

        pg.init()
        # Init game window
        pg.display.set_caption(caption)
        self.display_window = pg.display.set_mode(window_size)

        self.fps = pg.time.Clock()

        square_size = self.window_size[0] / self.board_size[0]
        self.board = Board((self.board_size[0], self.board_size[1]), square_size)

    def display(self, data):
        '''
        Display the matrix
        The input should be the data (matrix)
        '''
        self.draw_grid(data)

    def update(self, data):
        '''Update the display'''
        self.display(data)
        pg.display.update()

    def insert(self, pos, name):
        '''Insert a object into the map'''
        data = Objects().get_data(name)
        self.board.insert(pos, data.id)

    def draw_grid(self, data):
        '''Draw the grid on the screen'''
        self.board.draw(self.display_window, data)
