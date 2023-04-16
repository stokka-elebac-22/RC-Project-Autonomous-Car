'''Importing needed libraries'''
import pytest
from computer_vision.pathfinding.pathfinding import PathFinding
from computer_vision.environment.src.environment import Environment, ViewPointObject
from computer_vision.environment.src.a_star import AStar

class TestParametrized:
    '''
    DOC: Testing PathFinding
    '''

    @pytest.mark.parametrize('times, angles, expected', [
        ([1, 2, 4, 5], [0, 0, 1, -5], [[7, 5], [0.5, -5]]),
        ([0.5, 0.7, 1, 2], [-1, -2, 1, 2], [[1.2, 3], [-1.5, 1.5]]),
    ])
    def test_merge_similar_angles(self, times, angles, expected):
        '''Testing distance to point'''
        board_size = (60, 115)
        env_size = 20

        tension = 0
        velocity = 10

        view_point_object: ViewPointObject = {
            'view_point': None,
            'object_id': 10,
        }
        env = Environment(board_size, env_size, view_point_object)
        a_star = AStar()

        path_finding = PathFinding(
            env,
            a_star,
            tension,
            velocity
        )

        data = path_finding.merge_similar_angles(times, angles, 1)

        assert data['times'] == expected[0]
        assert data['angles'] == expected[1]
