'''Importing needed libraries'''
import pytest
from computer_vision.pathfinding.lib import get_abs_velo, get_angle, get_angle_diff

class TestParametrized:
    '''
    DOC: Testing helping functions
    '''

    @pytest.mark.parametrize('vec, expected', [([3, 4], 5), ([2.8, 3.4], 4.4045)])
    def test_get_abs_velo(self, vec, expected):
        '''Testing get_abs_velo method'''
        assert get_abs_velo(vec) == pytest.approx(expected, 0.001)

    @pytest.mark.parametrize('vec, expected', [
        ([3, 4], 36.87),
        ([-3, 4], -36.87),
        ([-3, -4], -143.13),
        ([3, -4], 143.13),
        ])
    def test_get_angle(self, vec, expected):
        '''Testing get_angle method'''
        assert get_angle(vec) == pytest.approx(expected, 0.001)

    @pytest.mark.parametrize('angles, expected', [
        ([40, 45], [40, 5]),
        ([40, 35], [40, -5]),
        ([20, 30, 35], [20, 10, 5]),
        ([175, -175], [175, 10]),
        ([-175, 175], [-175, -10])
    ])
    def test_get_angle_diff(self, angles, expected):
        '''Get the list of change in angle'''
        assert get_angle_diff(angles) == expected