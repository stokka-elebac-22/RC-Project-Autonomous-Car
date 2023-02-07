"""Importing needed libraries"""
import pytest
from computer_vision.pathfinding.main import PathFinding

class TestParametrized:
    """
    DOC: Testing PathFinding
    """

    @pytest.mark.parametrize('point, expected', [((20, 300), (-1013.33, 200.0))])
    def test_point_to_distance(self, point, expected):
        '''Testing point to distance'''
        pathfinding = PathFinding(
            size= (60, 115),
            w_size= 720,
            pixel_height=500,
            pixel_width=300,
            cam_width=800,
            cam_height=500,
            cam_center=(800, 500),
            object_id=10
        )
        result = pathfinding.point_to_distance(point)
        assert result[0] == pytest.approx(expected[0], 0.001)
        assert result[1] == pytest.approx(expected[1], 0.001)
