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
        ((20, 300), (-1013.33, 200.0)),
        ((10, 50), (-1040.0, 450.0))])

    def test_point_to_distance(self, point, expected):
        '''Testing point to distance'''
        board_size = (60, 115)
        pixel_size = (300, 500)
        cam_size = (800, 500)
        cam_center = (800, 500)
        env_size = 20

        view_point_object: ViewPointObject = {
            'view_point': None,
            'object_id': 10,
        }
        env = Environment(board_size, env_size, view_point_object)
        a_star = AStar()

        pathfinding = PathFinding(
            pixel_size,
            cam_size,
            cam_center,
            env,
            a_star
        )

        result = pathfinding.point_to_distance(point)
        assert result[0] == pytest.approx(expected[0], 0.001)
        assert result[1] == pytest.approx(expected[1], 0.001)

    @pytest.mark.parametrize('distance, expected', [
        ((-1013.33, 200.0), (20, 300)),
        ((-1040.0, 450.0), (10, 50))])

    def test_distance_to_point(self, distance, expected):
        '''Testing distance to point'''
        board_size = (60, 115)
        pixel_size = (300, 500)
        cam_size = (800, 500)
        cam_center = (800, 500)
        env_size = 20

        view_point_object: ViewPointObject = {
            'view_point': None,
            'object_id': 10,
        }
        env = Environment(board_size, env_size, view_point_object)
        a_star = AStar()

        pathfinding = PathFinding(
            pixel_size,
            cam_size,
            cam_center,
            env,
            a_star
        )
        result = pathfinding.distance_to_point(distance)
        assert result[0] == pytest.approx(expected[0], 0.001)
        assert result[1] == pytest.approx(expected[1], 0.001)
