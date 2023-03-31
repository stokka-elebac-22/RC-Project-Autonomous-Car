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
        ((20, 300), (-98.71690549205113, 920.3376614349003)),
        ((10, 50), (-103.18577414502009, 893.8827273349013))])
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
