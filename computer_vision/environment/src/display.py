'''Display environment'''
import pygame as pg
from board import Board

class DisplayEnvironment:
    '''Displaying the environment with pygame'''
    def __init__(self, window_size, board_size, parameters, caption=''):
        self.window_size = window_size
        self.board_size = board_size

        pg.init()
        # Init game window
        pg.display.set_caption(caption)
        self.display_window = pg.display.set_mode(window_size)

        self.fps = pg.time.Clock()

        square_size = self.window_size[0] / self.board_size[0]
        self.board = Board((self.board_size[0], self.board_size[1]), square_size, parameters)

    def display(self, data):
        '''
        Display the matrix
        The input should be the data (matrix)
        '''
        self.draw_grid()

    def update(self, data):
        '''Update the display'''
        self.display(data)
        pg.display.update()

    def insert(self, object=None):
        '''Insert a object into the map'''

    def draw_grid(self):
        '''Draw the grid on the screen'''
        self.board.draw_squares(self.display_window)
