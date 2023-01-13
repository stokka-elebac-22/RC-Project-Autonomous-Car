# test_qr_code.py
from computer_vision.qr_code.qr_code import PointSet, SideSet
import pytest

def test_points_update():
    """Testing points"""
    points = PointSet()
    points.update([0, 1, 2, 3])
    assert points.point0 == 0
    assert points.point1 == 1
    assert points.point2 == 2
    assert points.point3 == 3

def test_sides_update():
    """Testing sides"""
    sides = SideSet()
    points = PointSet([[0, 0], [0, 2], [0, 3], [0, 1]])
    sides.update(points)
    assert sides.side_a == 0
    assert sides.side_b == 1
    assert sides.side_c == 0
    assert sides.side_d == 1

# test on pictures with approx
# https://docs.pytest.org/en/4.6.x/reference.html
