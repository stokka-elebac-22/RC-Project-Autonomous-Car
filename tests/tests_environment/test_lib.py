'''Test the library'''
import pytest
from computer_vision.environment.src.lib import Objects, TwoWayDict

class TestObjects:
    '''Testing the objects'''
    def test_init(self):
        '''Testing init'''
        obj = Objects()
        assert obj.objects['None'] == 0

    @pytest.mark.parametrize(
        ['param', 'exp'],
        [
            (['foo', 0, 'green', 1], ['green', 1])
        ]
    )

    def test_get_data(self, param, exp):
        '''Testing getting the objects color'''
        obj = Objects()
        obj.objects[param[0]] = param[1]
        obj.object_data[0]['color'] = param[2]
        obj.object_data[0]['thickness'] = param[3]
        assert obj.get_data('foo')['color'] == exp[0] and \
            obj.get_data(0)['color'] == exp[0] and \
            obj.get_data(0)['thickness'] == exp[1]


class TestTwoWayDict:
    '''Testing two way dict'''
    def test_setitem(self):
        '''Testing inserting item'''
        twd = TwoWayDict()
        twd['foo'] = 'bar'
        assert twd['foo'] == 'bar' and twd['bar'] == 'foo'

    def test_delitem(self):
        '''Testing deleting item'''
        twd = TwoWayDict()
        twd['foo'] = 'bar'
        assert twd['foo'] == 'bar' and twd['bar'] == 'foo'
        del twd['foo']
        with pytest.raises(Exception):
            _ = twd['foo']
            _ = twd['bar']

    def test_len(self):
        '''Testing the number fo connections'''
        twd = TwoWayDict()
        twd['foo'] = 'bar'
        assert len(twd) == 1
