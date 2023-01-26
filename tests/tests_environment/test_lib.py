'''Test the library'''
import pytest
from computer_vision.environment.src.lib import \
    Objects, Object, TwoWayDict, Node, binary_search_node

class TestObjects:
    '''Testing the objects'''
    def test_init(self):
        '''Testing init'''
        obj = Objects()
        assert obj.objects['None'] == 0

    @pytest.mark.parametrize(
        ['param', 'exp'],
        [
            (['foo', 1000, 'green', 1], ['green', 1])
        ]
    )

    def test_get_data(self, param, exp):
        '''Testing getting the objects color'''
        obj = Objects()
        obj.objects[param[0]] = param[1]
        params = {
            'color': param[2],
            'thickness': param[3]
        }
        obj.object_data[param[1]] = Object(param[1], param[0], params)
        assert obj.get_data(param[0]).color == exp[0]


class TestTwoWayDict:
    '''Testing two way dict'''
    def test_setitem(self):
        '''Testing inserting item'''
        twd = TwoWayDict()
        twd['foo'] = 'bar'
        twd[0] = 'foo0'
        assert twd['foo'] == 'bar' and twd['bar'] == 'foo' and \
            twd[0] == 'foo0'

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
class TestNode:
    '''Test node'''
    def test_node(self):
        '''Test Node'''
        node = Node((0, 0))
        assert node.parent is None
        parent = Node((0, 1))
        node.parent = parent
        assert node.parent.position == (0, 1)
        node_dup = Node((0, 0))
        assert node == node_dup

@pytest.mark.parametrize(
    ['arr', 'exp'],
    [
        ([
            [Node(f_value=0), Node(f_value=1), Node(f_value=2), Node(f_value=4)],
            Node(f_value=3)], 3),
        ([
            [Node(f_value=1)], Node(f_value=0)], 0)
    ]
)
def test_binary_search_node(arr, exp):
    '''Test binary search for nodes'''
    assert binary_search_node(arr[0], arr[1]) == exp
