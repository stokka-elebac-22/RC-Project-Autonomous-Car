'''Creating the board'''
import pygame as pg
from lib import Objects

class Board:
    '''Display Board'''
    def __init__(self, dimensions, square_size, parameters):
        self.rows = dimensions[0]
        self.cols = dimensions[1]
        self.square_size = square_size
        if parameters['thickness'] is None:
            self.thickness = 1
        else:
            self.thickness = parameters['thickness']
        self.board = self.create_board()

    def draw_squares(self, window):
        '''Draw the squares'''
        window.fill(pg.Color(255, 255, 255))
        for i, row in enumerate(self.board):
            for j in range(len(row)):
                color = pg.Color(0, 0, 0)
                pg.draw.rect(
                    window,
                    color,
                    pg.Rect(
                        self.square_size * i,
                        self.square_size * j,
                        self.square_size,
                        self.square_size),
                        self.thickness)

    def create_board(self):
        '''Creating the board'''
        board = []
        for _ in range(self.rows):
            tmp = []
            for _ in range(self.cols):
                tmp.append(0)
            board.append(tmp)
        return board

    def draw(self, window):
        '''Draw'''
        for i, row in enumerate(self.board):
            for j, col in enumerate(row):
                color = Objects().get_color(col)
                pg.draw.rect(
                    window,
                    color,
                    pg.Rect(
                        self.square_size * i,
                        self.square_size * j,
                        self.square_size,
                        self.square_size),
                        self.thickness)
        self.draw_squares(window)
