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
    @pytest.mark.skip(reason="no way of testing this without a video device")
    def test_init(self, size, exp):
        '''Testing the init method'''
        env = Environment(size, 1)
        assert env.size == (exp, exp) and len(env.map) == exp and len(env.map[0]) == exp

    @pytest.mark.parametrize(
        ['param', 'exp'],
        [
            ([(3, 3), None, 1, (0, 2), 1], [True, [[0,1,0],[0,0,0],[0,0,0]]]),
            ([(3, 3), None, 1, (0, 1), 1], [True, [[0,0,0],[0,1,0],[0,0,0]]]),
            ([(3, 3), None, 1, (3, 3), 1], [False, [[0,0,0],[0,0,0],[0,0,0]]]),
            ([(3, 3), None, 2.5, (3, 5), 1], [True, [[0,0,1],[0,0,0],[0,0,0]]]),
            ([(3, 3), {'view_point': (2, 1),
                        'object_id': 2},
                        2.5, (3, 8), 1], [False, [[0,0,0],[0,0,0],[0,2,0]]]),
            ([(3, 3), {'view_point': (2, 1),
                        'object_id': 2},
                        2.5, (3, 7), 1], [True, [[0,0,1],[0,0,0],[0,2,0]]]),
            ([(3, 3), None, 2.5, (-2, 5), 1], [True, [[1,0,0],[0,0,0],[0,0,0]]]),
            ([(3, 3), {'view_point': (2, 1),
                        'object_id':2},
                        2.5, (3, -1), 1], [False, [[0,0,0],[0,0,0],[0,2,0]]]),
        ]
    )
    def test_insert(self, param, exp):
        '''Testing inserting object into the environment'''
        env = Environment(param[0], param[2], param[1])
        ret = env.insert(param[3], param[4])
        data = env.get_data()
        assert ret == exp[0] and are_same(data, exp[1])

    @pytest.mark.parametrize(
        ['param', 'exp'],
        [
            ([(3, 3), None, 1, [(0, 2)], [1], 1, False], [[0,0,0],[0,0,0],[0,0,0]]),
            ([(3, 3), None, 1, [(0, 1), (1, 1), (1, 0)], [1, 1, 1], 1, True],
                [[0,0,0],[0,0,0],[0,0,0]]),
            ([(3, 3), None, 1, [(0, 1), (1, 1), (0, 2)], [1, 1, 1], 1, False],
                [[0,0,0],[0,1,1],[0,0,0]]),
            ([(3, 3), None, 1, [(0, 1), (1, 1), (1, 2)], [1, 1, 2], 1, True],
                [[0,0,2],[0,0,0],[0,0,0]]),
        ]
    )

    def test_remove(self, param, exp):
        '''Testing removing object(s)'''
        env = Environment(param[0], param[2], param[1])
        for pos, obj_id in zip(param[3], param[4]):
            env.insert(pos, obj_id)
        env.remove(param[5], param[6])
        data = env.get_data()
        print(data)
        assert are_same(data, exp)



    @pytest.mark.parametrize(
        ['param', 'exp'],
        [
            ([(3, 3), None, 1, (0, 0), 1], [True, [[1,0,0],[0,0,0],[0,0,0]]]),
            ([(3, 3), None, 1, (1, 1), 1], [True, [[0,0,0],[0,1,0],[0,0,0]]]),
            ([(3, 3), None, 1, (3, 3), 1], [False, [[0,0,0],[0,0,0],[0,0,0]]]),
            ([(3, 3), None, 2.5, (0, 2), 1], [True, [[0,0,1],[0,0,0],[0,0,0]]]),
            ([(3, 3), {'view_point': (2,1),
                        'object_id': 2}, 2.5, (3, 6), 1], [False, [[0,0,0],[0,0,0],[0,2,0]]]),
            ([(3, 3), None, 2.5, (-2, 5), 1], [False, [[0,0,0],[0,0,0],[0,0,0]]]),
            ([(3, 3), {'view_point': (2,1),
                        'object_id': 2}, 2.5, (3, -1), 1], [False, [[0,0,0],[0,0,0],[0,2,0]]]),
        ]
    )

    def test_insert_by_index(self, param, exp):
        '''Testing inserting object by index into the environment'''
        env = Environment(param[0], param[2], param[1])
        ret = env.insert_by_index(param[3], param[4])
        data = env.get_data()
        assert ret == exp[0] and are_same(data, exp[1])

    @pytest.mark.parametrize(
        ['param', 'exp'],
        [
            ([(3, 4), 1], None),
            ([(2, 4), 1], (0, 4)),
        ]
    )

    def test_get_pos(self, param, exp):
        '''Test find position of object'''
        env = Environment((5, 5), 1)
        env.insert(param[0], param[1])
        pos = env.get_pos(param[1])
        assert pos == exp

def are_same(mat1: np.array, mat2: np.array):
    '''Checks if matrix 1 and matrix 2 are identical'''
    if len(mat1) != len(mat2) or len(mat1[0]) != len(mat2[0]):
        return False

    for row1, row2 in zip(mat1, mat2):
        for col1, col2 in zip(row1, row2):
            if col1 != col2:
                return False
    return True
