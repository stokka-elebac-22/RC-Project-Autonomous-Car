'''Importing needed libraries'''
import pytest
from computer_vision.pathfinding.lib import PathFinding

class TestParametrized:
    '''
    DOC: Testing PathFinding Lib
    '''

    # SHOULD FAIL WHEN CHANGED LATER
    @pytest.mark.parametrize('point, expected', [
        ((20, 300), (-346.6666666, 1.21355)),
        ((10, 50), (-373.3333333, 1.5636))])
    def test_point_to_distance(self, point, expected):
        '''Testing point to distance'''
        pathfinding = PathFinding(
            size= (60, 115),
            pixel_height=500,
            pixel_width=300,
            cam_width=800,
            cam_height=500,
            object_id=10
        )
        result = pathfinding.point_to_distance(point)
        assert result[0] == pytest.approx(expected[0], 0.001)
        assert result[1] == pytest.approx(expected[1], 0.001)

    # SHOULD FAIL WHEN CHANGED LATER
    @pytest.mark.parametrize('distance, expected', [
        ((-1013.33, 200.0), (-230, 300)),
        ((-1040.0, 450.0), (-240, 50))])
    def test_distance_to_point(self, distance, expected):
        '''Testing distance to point'''
        pathfinding = PathFinding(
            size= (60, 115),
            pixel_height=500,
            pixel_width=300,
            cam_width=800,
            cam_height=500,
            object_id=10
        )
        result = pathfinding.distance_to_point(distance)
        assert result[0] == pytest.approx(expected[0], 0.001)
        assert result[1] == pytest.approx(expected[1], 0.001)
