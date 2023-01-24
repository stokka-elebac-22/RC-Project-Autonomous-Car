'''Test the library'''
from computer_vision.environment.src.lib import Objects, TwoWayDict

class TestObjects:
    '''Testing the objects'''
    def test_init(self):
        '''Testing init'''
        obj = Objects()
        assert obj.objects['None'] == 0 and len(obj.object_color[0]) == 1


    def test_get_color(self):
        '''Testing getting the objects color'''
        obj = Objects()
        obj.objects['foo'] = 0
        obj.object_color['foo'] = 'green'
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
        assert twd['foo'] is None and twd['bar'] is None

    def test_len(self):
        '''Testing the number fo connections'''
        twd = TwoWayDict()
        twd['foo'] = 'bar'
        assert len(twd) == 1
