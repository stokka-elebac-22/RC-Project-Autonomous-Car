'''Display environment'''
import pygame as pg
from board import Board
from lib import Objects

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

        square_size = self.window_size[1] / self.board_size[0]
        self.board = Board((self.board_size[1], self.board_size[0]), square_size)

    def display(self):
        '''
        Display the matrix
        '''
        # Draw the grid on the screen
        self.board.draw(self.display_window)

    def update(self, data):
        '''Update the display'''
        self.board.reset(data)
        pg.display.update()

    def insert(self, pos, name):
        '''Insert an object into the map'''
        object_data = Objects().get_data(name)
        self.board.insert(pos, object_data.id)
