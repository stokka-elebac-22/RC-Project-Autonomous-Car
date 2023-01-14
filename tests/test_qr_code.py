"""TEST"""
# test_qr_code.py
import pytest
from computer_vision.qr_code.qr_code import QRGeometry

def test_points_empty():
    """Testing points"""
    qr_code = QRGeometry()
    assert qr_code.points[0] == [0, 0] and qr_code.points[1] == [0, 0] and \
            qr_code.points[2] == [0, 0] and qr_code.points[3] == [0, 0]

@pytest.mark.parametrize(
    ["pts", "exp"],
    [
        ([[0, 0], [0, 1], [1, 1], [1, 0]], [[0, 0], [0, 1], [1, 1], [1, 0]]),
        ([[3, 1], [2, 4], [1, 4], [4, 1]], [[3, 1], [2, 4], [1, 4], [4, 1]]),
        ([[4, 6], [7, 1], [1, 2], [4, 4]], [[4, 6], [7, 1], [1, 2], [4, 4]])
    ]
)
def test_points_update(pts, exp):
    """Testing update points"""
    qr_code = QRGeometry(pts)
    assert qr_code.points[0] == exp[0] and qr_code.points[1] == exp[1] and \
            qr_code.points[2] == exp[2] and qr_code.points[3] == exp[3]

@pytest.mark.parametrize(
    ["pts", "exp"],
    [
        ([[0, 0], [1, 0], [1, 1], [0, 1]], [1, 1, 1, 1]),
        ([[2,-2], [-1, -1], [-2, 2], [1, 3]], [3, 3, 3, 5]),
        ([[18, 7], [7, 3], [4, 9], [17, 14]], [11, 6, 13, 7])
    ]
)
def test_sides_update(pts, exp):
    """Testing sides"""
    qr_code = QRGeometry(pts)
    assert qr_code.side_a == exp[0] and qr_code.side_b == exp[1] and \
        qr_code.side_c == exp[2] and qr_code.side_d == exp[3]

# test on pictures with approx
# https://docs.pytest.org/en/4.6.x/reference.html
