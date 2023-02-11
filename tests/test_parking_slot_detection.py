'''Importing needed libraries'''
import pytest
import cv2
import numpy as np
from computer_vision.line_detection.parking_slot_detection import ParkingSlotDetector
from computer_vision.qr_code.qr_code import QRCode

PATH = 'computer_vision/line_detection/assets/parking/'

class TestParametrized:
    '''
    DOC: Testing ParkingSlotDetector class from module line_detection
    '''

    def get_image(self, source):
        '''Helping function for tests to get a cv2 image from a source file'''
        image = cv2.imread(PATH + source)
        return image

    @pytest.mark.parametrize('lines, expected', [
        ([np.array((20, 120, 400, 20)), np.array((20, 120, 400, 20)),
        np.array((123, 232, 234, 100))],
         [[[(-0.26315789473684215, 125.26315789473688),
            (-0.26315789473684215, 125.26315789473688)],
             [(-1.1891891891891888, 378.27027027027015)]],
            [[np.array([20, 120, 400,  20]), np.array([20, 120, 400,  20])],
             [np.array([123, 232, 234, 100])]]]),
    ])
    def test_cluster_lines(self, lines, expected):
        '''Test cluster_lines method of ParkingSlotDetector'''
        parking_slot_detector = ParkingSlotDetector()
        clustered_lines, clustered_coords = parking_slot_detector.cluster_lines(
            lines)
        for i, line in enumerate(clustered_lines):
            for j, value in enumerate(line):
                assert value == pytest.approx(expected[0][i][j], 0.001)
        for i, coords in enumerate(clustered_coords):
            assert (np.array(coords) == np.array(expected[1][i])).all()

    @pytest.mark.parametrize('lines, coords, expected', [
        ([[-1, 100], [1, 2]], [[123, 123, 321, 321], [123, 123, 321, 321]],
         [[[-1, 100], [1, 2]], [[123, 123, 321, 321], [123, 123, 321, 321]]]),
        ([[-1, 100], [1, 200]], [[123, 123, 321, 321], [123, 123, 321, 321]],
        [[[-1, 100], [1, 200]], [[123, 123, 321, 321], [123, 123, 321, 321]]])
    ])
    def test_filter_lines(self, lines, coords, expected):
        '''Test filter_lines method of ParkingSlotDetector'''
        parking_slot_detector = ParkingSlotDetector()
        parking_slot_detector.filter_lines(lines, coords)
        assert lines == expected[0]
        assert coords == expected[1]

    @pytest.mark.parametrize('coordinates, expected', [(
        [(100, 200, 400, 800), (300, 400, 900, 200), (150, 500, 300, 100)],
        [100, 900]),
        ([(100, 200, 400, 800), (300, 400, 900, 200), (150, 500, 300, 100), (50, 120, 300, 400)],
         [50, 900]),
    ])
    def test_get_min_max_x(self, coordinates, expected):
        '''Test get_min_max_x method of ParkingSlotDetector'''
        parking_slot_detector = ParkingSlotDetector()
        min_x, max_x = parking_slot_detector.get_min_max_x(coordinates)
        assert min_x == expected[0]
        assert max_x == expected[1]

    @pytest.mark.parametrize('line_coords, points, expected', [
        ([np.array([100, 200, 300, 400]), np.array([200, 300, 400, 500])],
         [[10, 20], [20, 30], [40, 50], [50, 60]],
         [np.array([100, 200, 300, 400]), np.array([100, 200, 300, 400])]),
        ([np.array([200, 100, 300, 400]), np.array([300, 200, 400, 500])],
         [[25, 20], [20, 30], [40, 50], [50, 60]],
         [np.array([200, 100, 300, 400]), np.array([200, 100, 300, 400])])
    ])
    def test_get_closest_line(self, line_coords, points, expected):
        '''Test get_closest_line method of ParkingSlotDetector'''
        parking_slot_detector = ParkingSlotDetector()
        lines = parking_slot_detector.get_closest_line(
            line_coords, points)
        for i, line in enumerate(lines):
            assert (line == expected[i]).all()

    @pytest.mark.parametrize('img_source', [
        ('4.png'),
        ('7.png'),
        ('8.png')
    ])
    def test_detect_parking_lines(self, img_source):
        '''Test parking_lines method of ParkingSlotDetector'''
        QR_SIZE_PX = 76
        QR_SIZE_MM = 52
        QR_DISTANCE = 500
        image = self.get_image(img_source)
        parking_slot_detector = ParkingSlotDetector()
        qr_code = QRCode(QR_SIZE_PX, QR_SIZE_MM, QR_DISTANCE)
        data = qr_code.get_data(image)
        qr_code_data = {
            'ret': data['ret'],
            'points': data['points']
        }
        lines = parking_slot_detector.detect_parking_lines(
            image, qr_code_data)
        assert len(lines) > 0

    @pytest.mark.parametrize('min_x, max_x, line_parameters, expected', [
        (200, 400, [1, 50], np.array([200, 250, 400, 450])),
        (100, 300, [-1, 20], np.array([100, -80, 300, -280]))
    ])
    def test_get_line_coordinates_from_parameters(self, min_x, max_x, line_parameters, expected):
        '''Test get_line_coordinates_from_parameters method of ParkingSlotDetector'''
        parking_slot_detector = ParkingSlotDetector()
        line_coordinates = parking_slot_detector.get_line_coordinates_from_parameters(
            min_x, max_x, line_parameters)
        assert (line_coordinates == expected).all()

    @pytest.mark.parametrize('lines, expected', [
        ([
            np.array([200, 100, 300, 400]),
            np.array([200, 100, 300, 400])],
            np.array([200, 100, 200, 100])),
        ([
            np.array([100, 200, 300, 400]),
            np.array([200, 300, 400, 500])],
            np.array([100, 200, 200, 300]))
        ])
    def test_get_closing_line_of_two_lines(self, lines, expected):
        '''Test get_closing_line_of_two_lines method of ParkingSlotDetector'''
        parking_slot_detector = ParkingSlotDetector()
        closing_line = parking_slot_detector.get_closing_line_of_two_lines(lines)
        assert (closing_line == expected).all()
