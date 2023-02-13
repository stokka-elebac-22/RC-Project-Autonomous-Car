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
                Node({'position': (0, 1), 'h_value': 1, 'parent':
                Node({'position': (1, 1), 'h_value': 1, 'parent':
                Node({'position': (2, 1), 'h_value': 1})})})
            ),
            ([(2, 2), (0, 2),
                [
                    [0, 0, 0],
                    [0, 1, 1],
                    [0, 0, 0],
                ]],
                    Node({'position': (0, 2), 'h_value': 1, 'parent':
                    Node({'position': (0, 1), 'h_value': 1, 'parent':
                    Node({'position': (1, 0), 'h_value': 1, 'parent':
                    Node({'position': (2, 1), 'h_value': 1, 'parent':
                    Node({'position': (2, 2), 'h_value': 1})})})})})
            ),
            ([(0, 4), (4, 3),
                [
                    [0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0],
                    [0, 1, 1, 0, 0],
                    [0, 0, 0, 0, 0],
                ]],
                    Node({'position': (4, 3), 'h_value': 1, 'parent':
                    Node({'position': (3, 3), 'h_value': 1, 'parent':
                    Node({'position': (2, 2), 'h_value': 1, 'parent':
                    Node({'position': (2, 1), 'h_value': 1, 'parent':
                    Node({'position': (1, 0), 'h_value': 1, 'parent':
                    Node({'position': (0, 1), 'h_value': 1, 'parent':
                    Node({'position': (0, 2), 'h_value': 1, 'parent':
                    Node({'position': (0, 3), 'h_value': 1, 'parent':
                    Node({'position': (0, 4), 'h_value': 1})})})})})})})})})
            ),
            ([(0, 0), (0, 4),
                [
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                ]],
                    Node({'position': (0, 4), 'h_value': 1, 'parent':
                    Node({'position': (0, 3), 'h_value': 1, 'parent':
                    Node({'position': (0, 2), 'h_value': 1, 'parent':
                    Node({'position': (0, 1), 'h_value': 1, 'parent':
                    Node({'position': (0, 0), 'h_value': 1})})})})})
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
                Node({'position': (2, 8), 'h_value': 1, 'parent':
                Node({'position': (2, 7), 'h_value': 1, 'parent':
                Node({'position': (2, 6), 'h_value': 1, 'parent':
                Node({'position': (2, 5), 'h_value': 1, 'parent':
                Node({'position': (2, 4), 'h_value': 1, 'parent':
                Node({'position': (2, 3), 'h_value': 1, 'parent':
                Node({'position': (2, 2), 'h_value': 1, 'parent':
                Node({'position': (3, 1), 'h_value': 1, 'parent':
                Node({'position': (4, 1), 'h_value': 1, 'parent':
                Node({'position': (5, 1), 'h_value': 1, 'parent':
                Node({'position': (6, 1), 'h_value': 1, 'parent':
                Node({'position': (7, 2), 'h_value': 1, 'parent':
                Node({'position': (8, 3), 'h_value': 1, 'parent':
                Node({'position': (9, 4), 'h_value': 1, 'parent':
                Node({'position': (9, 5), 'h_value': 1 })})})})})})})})})})})})})})}),
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
                Node({'position': (2, 8), 'h_value': 1, 'parent':
                Node({'position': (2, 7), 'h_value': 1, 'parent':
                Node({'position': (2, 6), 'h_value': 1, 'parent':
                Node({'position': (2, 5), 'h_value': 1, 'parent':
                Node({'position': (2, 4), 'h_value': 1, 'parent':
                Node({'position': (2, 3), 'h_value': 1, 'parent':
                Node({'position': (2, 2), 'h_value': 1, 'parent':
                Node({'position': (3, 1), 'h_value': 1, 'parent':
                Node({'position': (4, 1), 'h_value': 1, 'parent':
                Node({'position': (5, 1), 'h_value': 1, 'parent':
                Node({'position': (6, 1), 'h_value': 1, 'parent':
                Node({'position': (7, 2), 'h_value': 1, 'parent':
                Node({'position': (8, 3), 'h_value': 1, 'parent':
                Node({'position': (9, 4), 'h_value': 1, 'parent':
                Node({'position': (9, 5), 'h_value': 1 })})})})})})})})})})})})})})}),
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
                Node({'position': (3, 7), 'h_value': 1, 'parent':
                Node({'position': (3, 6), 'h_value': 1, 'parent':
                Node({'position': (4, 5), 'h_value': 1, 'parent':
                Node({'position': (5, 5), 'h_value': 1, 'parent':
                Node({'position': (6, 5), 'h_value': 1, 'parent':
                Node({'position': (7, 5), 'h_value': 1, 'parent':
                Node({'position': (8, 5), 'h_value': 1, 'parent':
                Node({'position': (9, 5), 'h_value': 1 })})})})})})})}),
            ),
            ([(0, 1), (1, 2),
            [
                [0, 0, 1],
                [0, 1, 0],
                [0, 0, 0],
            ]],
                Node({'position': (1, 2), 'h_value': 1, 'parent':
                Node({'position': (2, 1), 'h_value': 1, 'parent':
                Node({'position': (1, 0), 'h_value': 1, 'parent':
                Node({'position': (0, 1), 'h_value': 1 })})})}),
            ),
            ([(1, 2), (0, 1),
            [
                [0, 0, 1],
                [0, 1, 0],
                [0, 0, 0],
            ]],
                Node({'position': (0, 1), 'h_value': 1, 'parent':
                Node({'position': (1, 0), 'h_value': 1, 'parent':
                Node({'position': (2, 1), 'h_value': 1, 'parent':
                Node({'position': (1, 2), 'h_value': 1 })})})}),
            ),
            ([(0, 1), (1, 0),
            [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 0],
            ]],
                Node({'position': (1, 0), 'h_value': 1, 'parent':
                Node({'position': (2, 1), 'h_value': 1, 'parent':
                Node({'position': (1, 2), 'h_value': 1, 'parent':
                Node({'position': (0, 1), 'h_value': 1 })})})}),
            ),
            ([(1, 0), (0, 1),
            [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 0],
            ]],
                Node({'position': (0, 1), 'h_value': 1, 'parent':
                Node({'position': (1, 2), 'h_value': 1, 'parent':
                Node({'position': (2, 1), 'h_value': 1, 'parent':
                Node({'position': (1, 0), 'h_value': 1 })})})}),
            ),
            ([(1, 0), (0, 1),
            [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 0],
            ]],
                Node({'position': (0, 1), 'h_value': 1, 'parent':
                Node({'position': (1, 2), 'h_value': 1, 'parent':
                Node({'position': (2, 1), 'h_value': 1, 'parent':
                Node({'position': (1, 0), 'h_value': 1 })})})}),
            ),
        ]
    )
    def test_find_path(self, param, exp):
        '''Test find path'''
        a_star = AStar()
        cur_node: Node = a_star.find_path(param[2], param[0], param[1])
        cur_exp: Node = exp
        assert cur_node == cur_exp
        while True:
            print(cur_node.position, cur_exp.position)
            cur_node = cur_node.parent
            cur_exp = cur_exp.parent
            if cur_exp is None:
                return
            print(cur_node.position, cur_exp.position)
            assert cur_node == cur_exp

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

    def test_create_weighted_node_matrix(self, param, exp):
        '''Test create weight matrix'''
        a_star = AStar(param[0])
        res = a_star.create_weight_matrix(param[1])
        assert (exp[0] == res).all()
