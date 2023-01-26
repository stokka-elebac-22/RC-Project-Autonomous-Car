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
                Node((2, 1), parent=
                Node((1, 1), parent=
                Node((0, 1), parent=None)))
            ),
            ([(2, 2), (0, 2),
                [
                    [0, 0, 0],
                    [0, 1, 1],
                    [0, 0, 0],
                ]],
                    Node((2, 2), parent=
                    Node((2, 1), parent=
                    Node((1, 0), parent=
                    Node((0, 1), parent=
                    Node((0, 2), parent=None)))))
            )
        ]
    )
    def test_find_path(self, param, exp):
        '''Test find path'''
        a_star = AStar()
        cur_node: Node = a_star.find_path(param[2], param[0], param[1])
        cur_exp: Node = exp

        assert cur_node == cur_exp
        while cur_exp.parent is not None:
            cur_node = cur_node.parent
            cur_exp = cur_exp.parent
            assert cur_node == cur_exp
