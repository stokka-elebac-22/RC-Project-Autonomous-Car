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
    @pytest.mark.parametrize(
        ["name", "exp"],
        [
            ('angle_0_35_r', [True, 0]),
            ('angle_10_37_r', [True, 10]),
            ('angle_16_38_r', [True, 16]),
            ('angle_20_38_r', [True, 20]),
            ('angle_30_38_r', [True, 30]),
            ('angle_10_43_l', [True, -10]),
            ('angle_20_44_l', [True, -20]),
            # ('angle_30_36_l', [True, 30]), # not sure if that photo is correct
        ]
    )
    def test_angle_logi_1080p(self, name, exp):
        """Testing the angle to qr code"""
        qr_size_px = 112
        qr_size_mm = 52
        qr_distance = 400
        qr_code = QRCode(qr_size_px, qr_size_mm, qr_distance)
        frame = cv.imread("tests/images/qr_code/logi_1080p/angle/" + name + ".jpg")
        data = qr_code.get_data(frame)
        # Tolerance of 5
        assert data['ret'] == exp[0] and data['angles'][0] == pytest.approx(exp[1], abs=abs(5))

    @pytest.mark.parametrize(
        ['path', 'exp'],
        [
            ('distance_28', [True, 280, 0]),
            ('distance_30', [True, 300, 0]),
            ('distance_35', [True, 350, 0]),
            ('distance_40', [True, 400, 0]),
            ('distance_50', [True, 500, 0]),
            ('distance_52', [True, 520, 0]),
            ('distance_60', [True, 600, 0]),
        ]
    )

    def test_distance_logi_1080p(self, path, exp):
        '''Testing the distance to qr_code'''
        qr_size_px = 112
        qr_size_mm = 52
        qr_distance = 300
        qr_code = QRCode(qr_size_px, qr_size_mm, qr_distance)
        frame = cv.imread('tests/images/qr_code/logi_1080p/distance/' + path + '.jpg')
        data = qr_code.get_data(frame)
        # Tolerance of 30mm
        assert data['ret'] == exp[0] and data['distances'][0] == pytest.approx(exp[1], abs=abs(30)) \
            and data['angles'][0] == pytest.approx(exp[2], abs=abs(5))

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

    @pytest.mark.skip(reason='No way of testing atm because of poor test photos')
    def test_distance_webcam(self, path, exp):
        '''Testing the distance to qr code for the small webcam'''
        qr_size_px = 120
        qr_size_mm= 52
        qr_distance_mm = 320
        qr_code = QRCode(qr_size_px, qr_size_mm, qr_distance_mm)
        frame = cv.imread('tests/images/qr_code/webcam/distance/' + path + '.jpg')
        data = qr_code.get_data(frame)
        assert data['ret'] == exp[0] and data['distances']== pytest.approx(exp[1]) \
            and data['angles'] == pytest.approx(exp[2])

    @pytest.mark.parametrize(
        ['path', 'exp'],
        [('qrcode.png', [True, 3])]
    )

    def test_multiple(self, path, exp):
        '''Testing if the code can detect multiple qr codes'''
        qr_code = QRCode(1, 1, 1)
        frame = cv.imread('tests/images/qr_code/multi/' + path)
        data = qr_code.get_data(frame)
        print(data['ret'])
        assert data['ret'] == exp[0] and len(data['distances']) == exp[1]
