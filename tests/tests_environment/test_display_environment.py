'''Test the display for environment'''
import pytest
import pygame as pg
from computer_vision.environment.src.board import Board
from computer_vision.environment.src.display import DisplayEnvironment
class TestDisplayEnvironment:
    '''Testing the environment'''
    @pytest.mark.parametrize(
        ['param', 'exp'],
        [
            ([(1, 2), (10, 10)], [(1, 2), (10, 10)])
        ]
    )
    def test_init(self, param, exp):
        '''Testing the init method'''
        try:
            env = DisplayEnvironment(param[0], param[1])
            assert env.window_size == exp[0] and env.board_size == exp[1]
        except pg.error:
            pass

class TestBoard:
    '''Testing the board'''
    @pytest.mark.parametrize(
        ['param', 'exp'],
        [
            ([(10, 10), 1], [10, 10])
        ]
    )
    def test_init(self, param, exp):
        '''Testing init'''
        board = Board(param[0], param[1])
        assert board.rows == exp[0] and board.cols == exp[1]

    @pytest.mark.parametrize(
        ['param', 'exp'],
        [
            ([(10, 10), 1], [10, 10])
        ]
    )
    def test_create_board(self, param, exp):
        '''Testing creating board'''
        board = Board(param[0], param[1])
        board.create_board()
        assert len(board.board) == exp[0] and len(board.board[0]) == exp[1]
