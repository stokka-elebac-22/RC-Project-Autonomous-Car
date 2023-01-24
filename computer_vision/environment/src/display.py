'''Display environment'''
import pygame as pg
from .environment import Environment
from .board import Board

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

    def display(self, mat):
        '''
        Display the matrix
        The input should be the data (matrix)
        '''
        self.draw_grid((len(mat), len(mat[0])))

    def update(self, env: Environment):
        '''Update the display'''

    def insert(self, object=None):
        '''Insert a object into the map'''

    def draw_grid(self, size):
        '''Draw the grid on the screen'''

if __name__ == '__main__':
    environment = Environment(10)

    # Game loop
    while True:
        pass
