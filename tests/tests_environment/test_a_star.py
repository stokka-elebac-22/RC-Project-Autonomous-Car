'''A star'''
import pytest
from computer_vision.environment.src.a_star import AStar
from computer_vision.environment.src.lib import Node

class TestAStar:
    '''Test A*'''
    @pytest.mark.parametrize(
        ['param', 'exp'],
        [
            
            
            ([(2, 1), (0, 1),
            [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ]],
                Node((0, 1), 1, parent=
                Node((1, 1), 1, parent=
                Node((2, 1), 1, parent=None)))
            ),
            ([(2, 2), (0, 2),
                [
                    [0, 0, 0],
                    [0, 1, 1],
                    [0, 0, 0],
                ]],
                    Node((0, 2), 1, parent=
                    Node((0, 1), 1, parent=
                    Node((1, 0), 1, parent=
                    Node((2, 1), 1, parent=
                    Node((2, 2), 1, parent=None)))))
            ),
            ([(0, 4), (4, 3),
                [
                    [0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0],
                    [0, 1, 1, 0, 0],
                    [0, 0, 0, 0, 0],
                ]],
                    Node((4, 3), 1, parent=
                    Node((3, 3), 1, parent=
                    Node((2, 2), 1, parent=
                    Node((2, 1), 1, parent=
                    Node((1, 0), 1, parent=
                    Node((0, 1), 1, parent=
                    Node((0, 2), 1, parent=
                    Node((0, 3), 1, parent=
                    Node((0, 4), 1, parent=None)))))))))
            ),
            ([(0, 0), (0, 4),
                [
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                ]],
                    Node((0, 4), 1, parent=
                    Node((0, 3), 1, parent=
                    Node((0, 2), 1, parent=
                    Node((0, 1), 1, parent=
                    Node((0, 0), 1, parent=None)))))
            ),
            ([(9, 5), (2, 8),
            [
                [0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0],
                [0,0,1,1,1,1,1,1,1,1,1],
                [0,0,1,0,0,0,0,0,0,0,0],
                [0,0,1,0,0,0,0,0,0,0,0],
                [0,0,1,1,0,0,0,0,0,0,0],
                [0,0,0,1,1,0,0,0,0,0,0],
                [0,0,0,0,1,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0],
            ]],
                Node((2,8), 1, parent=
                Node((2,7), 1, parent=
                Node((2,6), 1, parent=
                Node((2,5), 1, parent=
                Node((2,4), 1, parent=
                Node((2,3), 1, parent=
                Node((2,2), 1, parent=
                Node((3,1), 1, parent=
                Node((4,1), 1, parent=
                Node((5,1), 1, parent=
                Node((6,1), 1, parent=
                Node((7,2), 1, parent=
                Node((8,3), 1, parent=
                Node((9,4), 1, parent=
                Node((9,5), 1, parent=None
                )))))))))))))))
            ),
            ([(9, 5), (2, 8),
            [
                [0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0],
                [0,0,1,1,1,1,1,1,1,1,1],
                [0,0,0,0,0,0,0,0,0,0,0],
                [0,0,1,0,0,0,0,0,0,0,0],
                [0,0,1,1,0,0,0,0,0,0,0],
                [0,0,0,1,1,0,0,0,0,0,0],
                [0,0,0,0,1,1,1,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0],
            ]],
                Node((2,8), 1, parent=
                Node((2,7), 1, parent=
                Node((2,6), 1, parent=
                Node((2,5), 1, parent=
                Node((2,4), 1, parent=
                Node((2,3), 1, parent=
                Node((2,2), 1, parent=
                Node((3,1), 1, parent=
                Node((4,1), 1, parent=
                Node((5,1), 1, parent=
                Node((6,1), 1, parent=
                Node((7,2), 1, parent=
                Node((8,3), 1, parent=
                Node((9,4), 1, parent=
                Node((9,5), 1, parent=None
                )))))))))))))))
            ),
            ([(9, 5), (3, 7),
            [
                [0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,1,1,1,1,1],
                [0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,1,1,1,1,1],
                [0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0],
            ]],
                Node((3,7), 1, parent=
                Node((3,6), 1, parent=
                Node((4,5), 1, parent=
                Node((5,5), 1, parent=
                Node((6,5), 1, parent=
                Node((7,5), 1, parent=
                Node((8,5), 1, parent=
                Node((9,5), 1, parent=None
                ))))))))
            ),
            ([(0, 1), (1, 2),
            [
                [0, 0, 1],
                [0, 1, 0],
                [0, 0, 0],
            ]],
                Node((1, 2), 1, parent=
                Node((2, 1), 1, parent=
                Node((1, 0), 1, parent=
                Node((0, 1), 1, parent=None))))
            ),
            ([(1, 2), (0, 1),
            [
                [0, 0, 1],
                [0, 1, 0],
                [0, 0, 0],
            ]],
                Node((0, 1), 1, parent=
                Node((1, 0), 1, parent=
                Node((2, 1), 1, parent=
                Node((1, 2), 1, parent=None))))
            ),
            ([(0, 1), (1, 0),
            [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 0],
            ]],
                Node((1, 0), 1, parent=
                Node((2, 1), 1, parent=
                Node((1, 2), 1, parent=
                Node((0, 1), 1, parent=None))))
            ),
            ([(1, 0), (0, 1),
            [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 0],
            ]],
                Node((0, 1), 1, parent=
                Node((1, 2), 1, parent=
                Node((2, 1), 1, parent=
                Node((1, 0), 1, parent=None))))
            ),
        ]
    )
    def test_find_path(self, param, exp):
        '''Test find path'''
        a_star = AStar()
        cur_node: Node = a_star.find_path(param[2], param[0], param[1])
        cur_exp: Node = exp
        print(cur_node.position, cur_exp.position)
        assert cur_node == cur_exp
        while True:
            cur_node = cur_node.parent
            cur_exp = cur_exp.parent
            if cur_exp is None:
                return
            print(cur_node.position, cur_exp.position)
            #assert cur_node == cur_exp

    @pytest.mark.parametrize(
        ['param', 'exp'],
        [
            ([1, [
                [0,0,0],
                [0,0,0],
                [0,0,0],
            ]],
            [[
                [0,0,0],
                [0,0,0],
                [0,0,0],
            ]]),
            ([1, [
                [0,1,0],
                [0,0,0],
                [0,0,0],
            ]],
            [[
                [1,2,1],
                [1,1,1],
                [0,0,0],
            ]]),
            ([1, [
                [0,1,0],
                [0,1,0],
                [0,0,0],
            ]],
            [[
                [2,3,2],
                [2,3,2],
                [1,1,1],
            ]]),
            ([2, [
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,1,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
            ]],
            [[
                [1,1,1,1,1],
                [1,2,2,2,1],
                [1,2,3,2,1],
                [1,2,2,2,1],
                [1,1,1,1,1],
            ]]),
            ([2, [
                [0,0,0,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
            ]],
            [[
                [2,3,3,3,2],
                [2,4,5,4,2],
                [2,4,5,4,2],
                [2,3,3,3,2],
                [1,1,1,1,1],
            ]]),
        ]
    )

    def test_create_weight_matrix(self, param, exp):
        '''Test create weight matrix'''
        a_star = AStar(param[0])
        res = a_star.create_weight_matrix(param[1])
        assert (exp[0] == res).all()
