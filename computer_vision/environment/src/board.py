'''Creating the board'''
import pygame as pg
from lib import Objects

class Board:
    '''Display Board'''
    def __init__(self, dimensions, square_size):
        self.rows = dimensions[0]
        self.cols = dimensions[1]
        self.square_size = square_size
        self.board = []
        self.create_board()

    def draw_squares(self, window):
        '''Draw the squares'''
        window.fill(pg.Color(255, 255, 255))

    def create_board(self):
        '''Creating the board'''
        for row in range(self.rows):
            self.board.append([])
            for _ in range(self.cols):
                self.board[row].append(0)

    def draw(self, surface):
        '''Draw'''
        for row in self.board:
            for col in self.board[row]:
                color = Objects().get_color([self.board[row][col]])
                pg.draw.rect(
                    surface,
                    color,
                    pg.Rect(
                        self.square_size * row,
                        self.square_size * col,
                        self.square_size,
                        self.square_size))
