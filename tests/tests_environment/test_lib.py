'''Test the library'''
import pytest
from computer_vision.environment.src.lib import \
    Objects, Object, TwoWayDict, Node, BinarySearchNode

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
        node = Node((0, 0), 1)
        assert node.parent is None
        parent = Node((0, 1), 1)
        node.parent = parent
        assert node.parent.position == (0, 1)
        node_dup = Node((0, 0), 1)
        assert node == node_dup

class TestBinarySearchNode:
    '''Test Binary Search Node class'''
    # @pytest.mark.parametrize(

    #     ['param', 'exp'],
    #     [
    #         ([
    #             [Node((0,0), 1, f_value=0),
    #             Node((0,0), 1, f_value=1),
    #             Node((0,0), 1, f_value=2),
    #             Node((0,0), 1, f_value=4)],
    #             Node((0,0), 1, f_value=3)], 3),
    #         ([
    #             [Node((0,0), 1, f_value=1)],
    #             Node((0,0), 1, f_value=0)], 0),
    #         ([
    #             [Node((0,0), 1, f_value=0)],
    #             Node((0,0), 1, f_value=1)], 1)
    #     ]
    # )
    # def test_binary_search_node(self, param, exp):
    #     '''Test binary search for nodes'''
    #     bsn = BinarySearchNode()
    #     assert bsn.__binary_search_node(param[0], param[1]) == exp # pylint: disable=protected-access

    @pytest.mark.parametrize(
        ['param', 'exp'],
        [
            ([
                [Node((0,0), 1, f_value=0),
                Node((0,0), 1, f_value=1),
                Node((0,0), 1, f_value=2),
                Node((0,0), 1, f_value=4)],
                Node((0,0), 1, f_value=3)],
                [Node((0,0), 1, f_value=0),
                Node((0,0), 1, f_value=1),
                Node((0,0), 1, f_value=2),
                Node((0,0), 1, f_value=3),
                Node((0,0), 1, f_value=4)],
                ),
            ([
                [Node((0,0), 1, f_value=1)],
                Node((0,0), 1, f_value=0)],
                [Node((0,0), 1, f_value=1),
                Node((0,0), 1, f_value=0)]),
            ([
                [Node((0,0), 1, f_value=0)],
                Node((0,0), 1, f_value=1)],
                [Node((0,0), 1, f_value=0),
                Node((0,0), 1, f_value=1)]),
            ([
                [Node((0,0), 1, f_value=4),
                Node((0,0), 1, f_value=2),
                Node((0,0), 1, f_value=3),
                Node((0,0), 1, f_value=8)],
                Node((0,0), 1, f_value=5)],
                [Node((0,0), 1, f_value=2),
                Node((0,0), 1, f_value=3),
                Node((0,0), 1, f_value=4),
                Node((0,0), 1, f_value=5),
                Node((0,0), 1, f_value=8)],
                ),
        ]
    )
    def test_insert(self, param, exp):
        '''Test insert'''
        bsn = BinarySearchNode()
        for node in param[0]:
            bsn.insert(node)
        bsn.insert(param[1])
        assert bsn.get() == exp

    @pytest.mark.parametrize(
        ['param', 'exp'],
        [
            (
            [Node((0,0), 1, f_value=4),
            Node((0,0), 1, f_value=2),
            Node((0,0), 1, f_value=3),
            Node((0,0), 1, f_value=8),
            Node((0,0), 1, f_value=5)],
            [[Node((0,0), 1, f_value=3),
            Node((0,0), 1, f_value=4),
            Node((0,0), 1, f_value=5),
            Node((0,0), 1, f_value=8)],
            [Node((0,0), 1, f_value=3),
            Node((0,0), 1, f_value=5),
            Node((0,0), 1, f_value=8)]],
            ),
        ]
    )
    def data1(self):
        '''
        A data function that generates data
        Each node gets a new id when generated and hence need to be 'reused' to get
        correct result/comparison
        '''
        node2 = Node((0,0), 1, f_value=2)
        node3 = Node((0,0), 1, f_value=3)
        node4 = Node((0,0), 1, f_value=4)
        node5 = Node((0,0), 1, f_value=5)
        node8 = Node((0,0), 1, f_value=8)

        param = [node4, node2, node3, node5, node8]

        exp = [
            [node3, node4, node5, node8],
            [node4, node5, node8],
        ]

        return param, exp

    def test_delete(self):
        '''Test delete'''
        param, exp = self.data1()
        bsn = BinarySearchNode()
        for node in param:
            bsn.insert(node)
        values = bsn.get()
        bsn.delete(values[0].id) # deleting the first element in the list
        assert bsn.get() == exp[0]

    def test_pop(self):
        '''Test pop'''
        param, exp = self.data1()
        bsn = BinarySearchNode()
        for node in param:
            bsn.insert(node)
        node = bsn.pop()
        assert bsn.get() == exp[0] and node is not None
        bsn.pop(1)
        assert bsn.get() == exp[1]
