'''Importing needed libraries'''
import pytest
from computer_vision.pathfinding.pathfinding import PathFinding
from computer_vision.environment.src.environment import Environment, ViewPointObject
from computer_vision.environment.src.a_star import AStar

class TestParametrized:
    '''
    DOC: Testing PathFinding
    '''

    @pytest.mark.parametrize('point, expected', [
        ((20, 300), (-66.17662952711039, 639.4140036278998)),
        ((10, 50), (-737.7092676379443, 2500))])
    def test_point_to_distance(self, point, expected):
        '''Testing point to distance'''
        board_size = (60, 115)
        env_size = 20
        pixel_width = 300
        pixel_height = 500

        tension = 0
        velocity = 10

        view_point_object: ViewPointObject = {
            'view_point': None,
            'object_id': 10,
        }
        env = Environment(board_size, env_size, view_point_object)
        a_star = AStar()

        path_finding = PathFinding(
            [pixel_width, pixel_height],
            env,
            a_star,
            tension,
            velocity
        )

        result = path_finding.point_to_distance(point)
        assert result[0] == pytest.approx(expected[0], 0.001)
        assert result[1] == pytest.approx(expected[1], 0.001)

    # SHOULD FAIL WHEN CHANGED LATER
    @pytest.mark.parametrize('distance, expected', [
        ((-1013.33, 200.0), (-714, 300)),
        ((-1040.0, 450.0), (-740, 50))])
    def test_distance_to_point(self, distance, expected):
        '''Testing distance to point'''
        board_size = (60, 115)
        env_size = 20
        pixel_width = 300
        pixel_height = 500

        tension = 0
        velocity = 10

        view_point_object: ViewPointObject = {
            'view_point': None,
            'object_id': 10,
        }
        env = Environment(board_size, env_size, view_point_object)
        a_star = AStar()

        path_finding = PathFinding(
            [pixel_width, pixel_height],
            env,
            a_star,
            tension,
            velocity
        )

        result = path_finding.distance_to_point(distance)
        assert result[0] == pytest.approx(expected[0], 0.001)
        assert result[1] == pytest.approx(expected[1], 0.001)

    @pytest.mark.parametrize('times, angles, expected', [
        ([1, 2, 4, 5], [0, 0, 1, -5], [[7, 5], [0.5, -5]]),
        ([0.5, 0.7, 1, 2], [-1, -2, 1, 2], [[1.2, 3], [-1.5, 1.5]]),
    ])
    def test_merge_similar_angles(self, times, angles, expected):
        '''Testing distance to point'''
        board_size = (60, 115)
        env_size = 20
        pixel_width = 300
        pixel_height = 500

        tension = 0
        velocity = 10

        view_point_object: ViewPointObject = {
            'view_point': None,
            'object_id': 10,
        }
        env = Environment(board_size, env_size, view_point_object)
        a_star = AStar()

        path_finding = PathFinding(
            [pixel_width, pixel_height],
            env,
            a_star,
            tension,
            velocity
        )

        data = path_finding.merge_similar_angles(times, angles, 1)

        assert data['times'] == expected[0]
        assert data['angles'] == expected[1]
