'''Test the environment'''
import pytest
import numpy as np
from computer_vision.environment.src.environment import Environment

class TestEnvironment:
    '''Testing the environment'''
    @pytest.mark.parametrize(
        ['size', 'exp'],
        [
            ((10, 10), 10)
        ]
    )
    def test_init(self, size, exp):
        '''Testing the init method'''
        env = Environment(size, 1)
        assert env.size == (exp, exp) and len(env.map) == exp and len(env.map[0]) == exp

    @pytest.mark.parametrize(
        ['param', 'exp'],
        [
            ([(3, 3), 2, 0, 0], [[0,1,0],[0,0,0],[0,0,0]])
        ]
    )
    def test_insert(self, param, exp):
        '''Testing inserting object into the environment'''
        env = Environment(param[0], 1)
        env.insert_object(param[1], param[2], param[3])
        data = env.get_data()
        assert are_same(data, exp)

def are_same(mat1: np.array, mat2: np.array):
    '''Checks if matrix 1 and matrix 2 are identical'''
    if len(mat1) != len(mat2) or len(mat1[0]) != len(mat2[0]):
        return False

    for row1, row2 in zip(mat1, mat2):
        for col1, col2 in zip(row1, row2):
            if col1 != col2:
                return False
    return True
