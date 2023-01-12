# test_qr_code.py
from computer_vision.qr_code.qr_code import Points, Sides
import pytest

def test_points_update():
    points = Points()
    points.update([0, 1, 2, 3])
    assert points.p0 == 0
    assert points.p1 == 1
    assert points.p2 == 2
    assert points.p3 == 3

def test_sides_update():
    sides = Sides()
    points = Points([[0, 0], [0, 2], [0, 3], [0, 1]])
    sides.update(points)
    assert sides.a == 0
    assert sides.b == 1
    assert sides.c == 0
    assert sides.d == 1

# test on pictures with approx
# https://docs.pytest.org/en/4.6.x/reference.html
