'''Test the environment'''
import pytest
from computer_vision.environment.src.environment import Environment

class TestEnvironment:
    '''Testing the environment'''
    @pytest.mark.parametrize(
        ['size', 'exp'],
        [
            (10, 10)
        ]
    )
    def test_init(self, size, exp):
        '''Testing the init method'''
        env = Environment(size)
        assert env.size == (exp, exp) and len(env.map) == exp and len(env.map[0]) == exp
