'''Test the environment'''
import pytest
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
        env = Environment(size)
        assert env.size == (exp, exp) and len(env.map) == exp and len(env.map[0]) == exp

    @pytest.mark.parametrize(
        ['param', 'exp'],
        [
            ([(3, 3), 2, 0, 0], [[0,1,0],[0,0,0],[0,0,0]])
        ]
    )
    def test_insert(self, param, exp):
        '''Testing inserting object into the environment'''
        env = Environment(param[0])
        env.insert_object(param[1], param[2], param[3])
        assert env.get_data() == exp
