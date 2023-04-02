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

    @pytest.mark.parametrize('point_one, point_two, expected', [
        ((32, 29), (31.5, 28.5625), -48.81),
        ((32, 29), (31.5, 29.4375), -131.19),
        ((32, 29), (32.5, 28.5625), 48.81),
        ((32, 29), (32.5, 29.4375), 131.19),
        ((31, 28), (31, 28), 0),
        ((31, 28), (31, 29), 0),
        ((31, 28), (31, 27), 0),
        ((31, 28), (30, 28), -90),
        ((31, 28), (32, 28), 90),
        ])
    def test_get_angle(self, point_one, point_two, expected):
        '''Testing get_angle method'''
        assert get_angle(point_one, point_two) == pytest.approx(expected, 0.001)

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
