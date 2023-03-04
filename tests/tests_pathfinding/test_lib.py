'''Importing needed libraries'''
import pytest
from computer_vision.pathfinding.lib import PathFinding

class TestParametrized:
    '''
    DOC: Testing PathFinding Lib
    '''

    # SHOULD FAIL WHEN CHANGED LATER
    @pytest.mark.parametrize('point, expected', [
        ((20, 300), (-28.32843655299916, 280.4886090479)),
        ((10, 50), (-94.51080737361255, 844.0957035229))])
    def test_point_to_distance(self, point, expected):
        '''Testing point to distance'''
        pathfinding = PathFinding(
            size= (60, 115),
            pixel_height=500,
            pixel_width=300,
            object_id=10
        )
        result = pathfinding.point_to_distance(point)
        assert result[0] == pytest.approx(expected[0], 0.001)
        assert result[1] == pytest.approx(expected[1], 0.001)

    # SHOULD FAIL WHEN CHANGED LATER
    @pytest.mark.parametrize('distance, expected', [
        ((-1013.33, 200.0), (-714, 300)),
        ((-1040.0, 450.0), (-740, 50))])
    def test_distance_to_point(self, distance, expected):
        '''Testing distance to point'''
        pathfinding = PathFinding(
            size= (60, 115),
            pixel_height=500,
            pixel_width=300,
            object_id=10
        )
        result = pathfinding.distance_to_point(distance)
        assert result[0] == pytest.approx(expected[0], 0.001)
        assert result[1] == pytest.approx(expected[1], 0.001)
