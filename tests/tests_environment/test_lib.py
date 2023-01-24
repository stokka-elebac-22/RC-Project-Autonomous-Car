'''Test the library'''
import pytest
from computer_vision.environment.src.lib import Objects, TwoWayDict

class TestObjects:
    '''Testing the objects'''
    def test_init(self):
        '''Testing init'''
        obj = Objects()
        assert obj.objects['None'] == 0


    def test_get_color(self):
        '''Testing getting the objects color'''
        obj = Objects()
        obj.objects['foo'] = 0
        obj.object_color[0] = 'green'
        assert obj.get_color('foo') == 'green' and obj.get_color(0) == 'green'


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
