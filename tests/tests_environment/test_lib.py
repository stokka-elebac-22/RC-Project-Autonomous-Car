'''Test the library'''
import pytest
from computer_vision.environment.src.lib import \
    Objects, Object, TwoWayDict, Node, BinarySearchList

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

class TestNode: # pylint: disable=R0903
    '''Test node'''
    def test_node(self):
        '''Test Node'''
        node = Node({'position': (0,0)})
        assert node.parent is None
        parent = Node({'position': (0,1)})
        node.parent = parent
        assert node.parent.position == (0, 1)
        node = Node({'position': (0,0)})
        node_dup = Node({'position': (0,0)})
        assert node == node_dup

class TestBinarySearchList:
    '''Test Binary Search List class'''
    @pytest.mark.parametrize(
        ['param', 'exp'],
        [
            ([
                [
                Node({'f_value': 0}),
                Node({'f_value': 1}),
                Node({'f_value': 2}),
                Node({'f_value': 4})],
                Node({'f_value': 3})],
                [
                Node({'f_value': 0}),
                Node({'f_value': 1}),
                Node({'f_value': 2}),
                Node({'f_value': 4}),
                Node({'f_value': 3})],
                ),
            ([
                [Node({'f_value': 1})],
                Node({'f_value': 0})],
                [Node({'f_value': 1}),
                Node({'f_value': 0})]),
            ([
                [Node({'f_value': 0})],
                Node({'f_value': 1})],
                [Node({'f_value': 0}),
                Node({'f_value': 1})]),
            ([
                [Node({'f_value': 4}),
                Node({'f_value': 2}),
                Node({'f_value': 3}),
                Node({'f_value': 8})],
                Node({'f_value': 5})],
                [Node({'f_value': 2}),
                Node({'f_value': 3}),
                Node({'f_value': 4}),
                Node({'f_value': 5}),
                Node({'f_value': 8})],
                ),
        ]
    )
    def test_insert(self, param, exp):
        '''Test insert'''
        bsn = BinarySearchList()
        print(param[0])
        for node in param[0]:
            bsn.insert(node)
        bsn.insert(param[1])
        _, nodes = bsn.get()
        assert nodes == exp

    def data1(self):
        '''A method to generate data'''
        node2 = Node({'f_value': 2})
        node3 = Node({'f_value': 3})
        node4 = Node({'f_value': 4})
        node5 = Node({'f_value': 5})
        node8 = Node({'f_value': 8})

        param = [node4, node2, node3, node5, node8]

        exp = [
            [node3, node4, node5, node8],
            [node4, node5, node8],
        ]

        return param, exp

    def test_delete(self):
        '''Test delete'''
        param, exp = self.data1()
        bsn = BinarySearchList()
        for node in param:
            bsn.insert(node)
        _, values = bsn.get()
        bsn.delete(values[0].position) # deleting the first element in the list
        _, nodes = bsn.get()
        assert nodes == exp[0]

    def test_pop(self):
        '''Test pop'''
        param, exp = self.data1()
        bsn = BinarySearchList()
        for node in param:
            bsn.insert(node)
        node = bsn.pop()
        _, nodes = bsn.get()
        assert nodes == exp[0] and node is not None
        bsn.pop(1)
        _, nodes = bsn.get()
        assert nodes == exp[1]

    @pytest.mark.parametrize(
        ['param', 'exp'],
        [
            ([Node({'position': (0,0), 'h_value': 1}), (0, 0), (0, 1)],
            [True, Node({'position': (0,0), 'h_value': 1}), False])
        ]
    )

    def test_get(self, param, exp):
        '''Test contains'''
        bsn = BinarySearchList()
        bsn.insert(param[0])
        ret, node = bsn.get(param[1])
        assert ret == exp[0] and node == exp[1] and bsn.get(param[2])[0] == exp[2]
