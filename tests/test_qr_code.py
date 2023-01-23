'''TEST'''
# test_qr_code.py
import pytest
import cv2 as cv
from computer_vision.qr_code.qr_code import QRGeometry, QRCode

class TestQRCode:
    '''Test QRCode'''
    def test_points_empty(self):
        '''Testing points'''
        qr_code = QRGeometry()
        assert qr_code.points[0] == [0, 0] and qr_code.points[1] == [0, 0] and \
                qr_code.points[2] == [0, 0] and qr_code.points[3] == [0, 0]

    @pytest.mark.parametrize(
        ['pts', 'exp'],
        [
            ([[0, 0], [0, 1], [1, 1], [1, 0]], [[0, 0], [0, 1], [1, 1], [1, 0]]),
            ([[3, 1], [2, 4], [1, 4], [4, 1]], [[3, 1], [2, 4], [1, 4], [4, 1]]),
            ([[4, 6], [7, 1], [1, 2], [4, 4]], [[4, 6], [7, 1], [1, 2], [4, 4]]),
        ]
    )
    def test_points_init(self, pts, exp):
        '''Testing init points'''
        qr_code = QRGeometry(pts=pts)
        assert qr_code.points[0] == exp[0] and qr_code.points[1] == exp[1] and \
                qr_code.points[2] == exp[2] and qr_code.points[3] == exp[3]

    @pytest.mark.parametrize(
        ['pts', 'exp'],
        [
            ([[0, 0], [0, 1], [1, 1], [1, 0]], [[0, 0], [0, 1], [1, 1], [1, 0]]),
            ([[3, 1], [2, 4], [1, 4], [4, 1]], [[3, 1], [2, 4], [1, 4], [4, 1]]),
            ([[4, 6], [7, 1], [1, 2], [4, 4]], [[4, 6], [7, 1], [1, 2], [4, 4]]),
        ]
    )
    def test_points_update(self, pts, exp):
        '''Testing update points'''
        qr_code = QRGeometry()
        qr_code.update(pts=pts)
        assert qr_code.points[0] == exp[0] and qr_code.points[1] == exp[1] and \
                qr_code.points[2] == exp[2] and qr_code.points[3] == exp[3]

    @pytest.mark.parametrize(
        ['pts', 'exp'],
        [
            ([[0, 0], [1, 0], [1, 1], [0, 1]], [1, 1, 1, 1]),
            ([[2,-2], [-1, -1], [-2, 2], [1, 3]], [3, 3, 3, 5]),
            ([[18, 7], [7, 3], [4, 9], [17, 14]], [11, 6, 13, 7])
        ]
    )
    def test_sides_update(self, pts, exp):
        '''Testing sides'''
        qr_code = QRGeometry(pts=pts)
        assert qr_code.side_a == exp[0] and qr_code.side_b == exp[1] and \
            qr_code.side_c == exp[2] and qr_code.side_d == exp[3]

    # test on pictures with approx
    # https://docs.pytest.org/en/4.6.x/reference.html
    # @pytest.mark.parametrize(
    #     ["name", "exp"],
    #     [
    #         ('DSC_0142', [True, 0]),
    #         ('DSC_0135', [True, 15]),
    #         ('DSC_0136', [True, 30]),
    #         ('DSC_0137', [True, 45]),
    #         ('DSC_0138', [False, None]),
    #         ('DSC_0141', [False, None]),
    #     ]
    # )
    # def test_angle(name, exp):
    #     """Testing the angle to qr code"""
    #     QR_SIZE_PX = 1500
    #     QR_SIZE_MM = 190
    #     QR_DISTANCE = 500
    #     qr_code = QRCode(QR_SIZE_PX, QR_SIZE_MM, QR_DISTANCE)
    #     frame = cv.imread("tests/images/qr_code/angle" + name + ".jpg")
    #     retval, _, angle, _, _, _ = qr_code.get_data(frame)
    #     assert retval == exp[0] and angle == pytest.approx(exp[1])

    @pytest.mark.parametrize(
        ['path', 'exp'],
        [
            ('distance_22', [True, 220, 0]),
            ('distance_32', [True, 320, 0]),
            ('distance_42', [True, 420, 0]),
            ('distance_53', [True, 530, 0]),
            ('distance_62', [True, 620, 0]),
            ('distance_82', [True, 820, 0]),
        ]
    )

    @pytest.mark.skip(reason='No way of testing atm')
    def test_distance_logi_1080p(self, path, exp):
        '''Testing the distance to qr_code'''
        qr_size_px = 52
        qr_size_mm= 52
        qr_distance_mm = 620
        qr_code = QRCode(qr_size_px, qr_size_mm, qr_distance_mm)
        frame = cv.imread('tests/images/qr_code/logi_1080p/distance/' + path + '.jpg')
        retval, distance, angle, _, _, _ = qr_code.get_data(frame)
        assert retval == exp[0] and distance == pytest.approx(exp[1]) \
            and angle == pytest.approx(exp[2])

    @pytest.mark.parametrize(
        ['path', 'exp'],
        [
            ('distance_22', [True, 220, 0]),
            ('distance_32', [True, 320, 0]),
            ('distance_42', [True, 420, 0]),
            ('distance_51', [True, 510, 0]),
            ('distance_53', [True, 530, 0]),
        ]
    )

    @pytest.mark.skip(reason='No way of testing atm')
    def test_distance_webcam(self, path, exp):
        '''Testing the distance to qr code for the small webcam'''
        qr_size_px = 120
        qr_size_mm= 52
        qr_distance_mm = 320
        qr_code = QRCode(qr_size_px, qr_size_mm, qr_distance_mm)
        frame = cv.imread('tests/images/qr_code/webcam/distance/' + path + '.jpg')
        retval, distance, angle, _, _, _ = qr_code.get_data(frame)
        assert retval == exp[0] and distance == pytest.approx(exp[1]) \
            and angle == pytest.approx(exp[2])

    @pytest.mark.parametrize(
        ['path', 'exp'],
        [
            ('qrcode.png', [True, 3])
        ]
    )

    def test_multiple(self, path, exp):
        '''Testing if the code can detect multiple qr codes'''
        qr_code = QRCode(1, 1, 1)
        frame = cv.imread('tests/images/qr_code/multi/' + path)
        retval, distances, _, _, _, _ = qr_code.get_data(frame)
        assert retval == exp[0] and len(distances) == exp[1]
