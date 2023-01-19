"""TEST"""
# test_qr_code.py
import pytest
import cv2 as cv
from computer_vision.qr_code.qr_code import QRGeometry, QRCode

def test_points_empty():
    """Testing points"""
    qr_code = QRGeometry()
    assert qr_code.points[0] == [0, 0] and qr_code.points[1] == [0, 0] and \
            qr_code.points[2] == [0, 0] and qr_code.points[3] == [0, 0]

@pytest.mark.parametrize(
    ["pts", "exp"],
    [
        ([[[0, 0], [0, 1], [1, 1], [1, 0]]], [[0, 0], [0, 1], [1, 1], [1, 0]]),
        ([[[3, 1], [2, 4], [1, 4], [4, 1]]], [[3, 1], [2, 4], [1, 4], [4, 1]]),
        ([[[4, 6], [7, 1], [1, 2], [4, 4]]], [[4, 6], [7, 1], [1, 2], [4, 4]]),
    ]
)
def test_points_update(pts, exp):
    """Testing update points"""
    qr_code = QRGeometry(pts=pts)
    assert qr_code.points[0] == exp[0] and qr_code.points[1] == exp[1] and \
            qr_code.points[2] == exp[2] and qr_code.points[3] == exp[3]

@pytest.mark.parametrize(
    ["pts", "exp"],
    [
        ([[[0, 0], [1, 0], [1, 1], [0, 1]]], [1, 1, 1, 1]),
        ([[[2,-2], [-1, -1], [-2, 2], [1, 3]]], [3, 3, 3, 5]),
        ([[[18, 7], [7, 3], [4, 9], [17, 14]]], [11, 6, 13, 7])
    ]
)
def test_sides_update(pts, exp):
    """Testing sides"""
    qr_code = QRGeometry(pts=pts)
    assert qr_code.side_a == exp[0] and qr_code.side_b == exp[1] and \
        qr_code.side_c == exp[2] and qr_code.side_d == exp[3]

# test on pictures with approx
# https://docs.pytest.org/en/4.6.x/reference.html
@pytest.mark.parametrize(
    ["name", "exp"],
    [
        ('DSC_0142', [True, 0]),
        ('DSC_0135', [True, 15]),
        ('DSC_0136', [True, 30]),
        ('DSC_0137', [True, 45]),
        ('DSC_0138', [False, 60]),
        ('DSC_0141', [False, 75]),
    ]
)
def test_angle(name, exp):
    """Testing the angle to qr code"""
    QR_SIZE_PX = 76
    QR_SIZE_MM = 52
    QR_DISTANCE = 500
    qr_code = QRCode(QR_SIZE_PX, QR_SIZE_MM, QR_DISTANCE)
    frame = cv.imread("tests/qr_test_img/" + name + ".jpg")
    retval, _, angle, _, _, _ = qr_code.get_data(frame)
    assert retval == exp[0] and angle == pytest.approx(exp[1])

@pytest.mark.parametrize(
    ["path", "exp"],
    [
        ('20', [True, 200, 0]),
        ('25', [True, 250, 0]),
        ('30', [True, 300, 0]),
        ('40', [True, 400, 0]),
        ('50', [True, 500, 0]),
        ('70', [True, 700, 0]),
        ('100', [True, 1000, 0]),
    ]
)

def test_distance(path, exp):
    """Testing the distance to qr_code"""
    QR_SIZE_PX = 76
    QR_SIZE_MM = 52
    QR_DISTANCE = 500
    qr_code = QRCode(QR_SIZE_PX, QR_SIZE_MM, QR_DISTANCE)
    frame = cv.imread("tests/qr_code/distance/" + path + ".jpg")
    retval, distance, angle, _, _, _ = qr_code.get_data(frame)
    assert retval == exp[0] and distance == pytest.approx(exp[1]) \
        and angle == pytest.approx(exp[2])
















