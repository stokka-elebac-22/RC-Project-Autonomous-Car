'''Importing needed libraries'''
import pytest
from computer_vision.pathfinding.lib import get_abs_velo

class TestParametrized:
    '''
    DOC: Testing helping functions
    '''

    @pytest.mark.parametrize('vec, expected', [([3, 4], 5), ([2.8, 3.4], 4.4045)])
    def test_get_abs_velo(self, vec, expected):
        '''Testing get_abs_velo method'''
        assert get_abs_velo(vec) == pytest.approx(expected, 0.001)
