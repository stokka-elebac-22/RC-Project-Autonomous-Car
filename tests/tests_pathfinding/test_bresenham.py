"""Importing needed libraries"""
import pytest
from computer_vision.pathfinding.bresenham import bresenham

class TestParametrized:
    """
    DOC: Testing bresenham function
    """

    @pytest.mark.parametrize('param, expected', [
        ([3, 4, 10, 2], [(3, 4), (4, 4), (5, 3), (6, 3), (7, 3), (8, 3), (9, 2), (10, 2)]),
        ([3, 4, 10, 7], [(3, 4), (4, 4), (5, 5), (6, 5), (7, 6), (8, 6), (9, 7), (10, 7)]),
        ([10, 2, 3, 4], [(10, 2), (9, 2), (8, 3), (7, 3), (6, 3), (5, 3), (4, 4), (3, 4)]),
        ([10, 7, 3, 4], [(10, 7), (9, 7), (8, 6), (7, 6), (6, 5), (5, 5), (4, 4), (3, 4)]),
        ])
    def test_bresenham(self, param, expected):
        '''Testing get_bresenham method'''
        assert bresenham(param[0], param[1], param[2], param[3]) == expected