"""Importing needed libraries"""
import pytest
import cv2
import numpy as np
from computer_vision.line_detection.lane_detection import LaneDetector
PATH = "computer_vision/line_detection/assets/"

class TestParametrized:
    """
    DOC: Testing TrafficSignDetection class from module traffic_sign_detection
    """

    def get_image(self, source):
        """Helping function for tests to get a cv2 image from a source file"""
        image = cv2.imread(PATH + source)
        return image

    @pytest.mark.parametrize('img_source', ['bike_park.jpg', 'curve.jpg', '1.jpg', '2.jpg'])
    def test_get_lane_region(self, img_source):
        """Test if the output image is not equal to the input image"""
        lane_detector = LaneDetector()
        original_image = self.get_image(img_source)

        new_image = lane_detector.get_region_of_interest(original_image)
        difference = cv2.subtract(original_image, new_image)
        b_color, g_color, r_color = cv2.split(difference)
        assert new_image.shape != original_image.shape or cv2.countNonZero(
            b_color) != 0 or cv2.countNonZero(g_color) != 0 or cv2.countNonZero(r_color) != 0

    @pytest.mark.parametrize('img_source, lines, expected', [
        ('bike_park.jpg', [np.array([300,327,1059,600]), np.array([0, 781, 272,561]), np.array([573,339,780,336])],[np.array([-0.412, 564.152]), np.array([0.3596837944664031, 219.09486166007926])]),
        ('curve.jpg', [np.array([751,327,1059,500]), np.array([0, 781, 272,561])], [np.array([-0.809, 781.0]), np.array([0.5616883116883115, -94.82792207792211])]),
        ('1.jpg', [np.array([123,434,343,767]), np.array([0, 781, 272,561]), np.array([394, 781, 122,561]), np.array([573,339,780,336])], [np.array([-0.4116581415174767,564.1521739130434]), np.array([1.161229946524065,355.0731283422457])]),
        ('2.jpg', [np.array([100,327,509,811])], [None, np.array([1.18337408, 208.66259169])])])
    def test_get_average_lines(self, img_source, lines, expected):
        """Test if the output average lines is equal to the expected average lines"""
        lane_detector = LaneDetector()
        image = self.get_image(img_source)
        avg_lines = lane_detector.get_average_lines(image, lines)

        if expected[0] is None:
           assert avg_lines[0] is None
        else:
            avg_lines[0] = np.array([np.round(i, 3) for i in avg_lines[0]])
            expected[0] = np.array([np.round(i, 3) for i in expected[0]])
            assert (avg_lines[0] == expected[0]).all()
        if expected[1] is None:
            assert avg_lines[1] is None
        else:
            avg_lines[1] = np.array([np.round(i, 3) for i in avg_lines[1]])
            expected[1] = np.array([np.round(i, 3) for i in expected[1]])
            assert (avg_lines[1] == expected[1]).all()

    @pytest.mark.parametrize('img_source, lines, expected', [
        ('bike_park.jpg', [np.array([300,327,1059,600]), np.array([0, 781, 272,561])], 92.5),
        ('curve.jpg', [np.array([751,327,1059,500]), np.array([0, 781, 272,561])], 81.225),
        ('1.jpg', [np.array([123,434,343,767]), np.array([0, 781, 272,561])], 96.925),
        ('2.jpg', [np.array([100,327,509,811]), np.array([573,339,780,336])], 83.175)])
    def test_get_diff_from_center_info(self, img_source, lines, expected):
        """Test if the output value is equal to the manual calculation value"""
        lane_detector = LaneDetector()
        image = self.get_image(img_source)
        diff = np.round(lane_detector.get_diff_from_center_info(image, lines), 3)
        assert diff == expected

    @pytest.mark.skip('NOT FINISHED')
    @pytest.mark.parametrize('img_source, lines, expected', [
        ('bike_park.jpg', [np.array([300,327,1059,600]), np.array([0, 781, 272,561])], [np.array([]), np.array([]), np.array([]), np.array([])]),
        ('curve.jpg', [np.array([751,327,1059,500]), np.array([0, 781, 272,561])], [np.array([]), np.array([]), np.array([]), np.array([])]),
        ('1.jpg', [np.array([123,434,343,767]), np.array([0, 781, 272,561])], [np.array([]), np.array([]), np.array([]), np.array([])]),
        ('2.jpg', [np.array([100,327,509,811]), np.array([0, 781, 272,561])], [(3000, 100, 3), np.array([[ 3.55484821e-01, -3.00399363e-01,  6.26821097e+01],
       [ 1.07330901e+01, -1.01749694e+01,  2.78875734e+03],
       [ 3.16837462e-03, -3.48181553e-03,  1.00000000e+00]]), np.array( [(2000, 3000), (1025, 2400), (50, 1800)]), np.array([np.array([ 6.31163708e-04, -1.29388560e+00,  3.06311637e+03]), np.array([-6.31163708e-04,  1.29388560e+00,  1.73688363e+03])])])])
    def test_get_course(self, img_source, lines, expected):
        """Test if the output value is equal to the manual calculation value"""
        lane_detector = LaneDetector()
        image = self.get_image(img_source)
        output_shape, matrix, coordinates, polys = lane_detector.get_course(
            image, lines)
        assert (output_shape == expected[0]).all()
        assert (matrix == expected[1]).all()
        assert (coordinates == expected[2]).all()
        assert (polys == expected[3]).all()

    @pytest.mark.skip('NOT FINISHED')
    @pytest.mark.parametrize('source, shape, points, transform, polys', [])
    def test_show_course(self, source, shape, points, transform, polys):
        """Test if the output value is equal to the manual calculation value"""
        lane_detector = LaneDetector()
        image = self.get_image(source)
        warped, weighted = lane_detector.show_course(
            image, shape, points, transform, polys)
        difference = cv2.subtract(warped, weighted)
        b_color, g_color, r_color = cv2.split(difference)
        assert warped.shape != weighted.shape or cv2.countNonZero(
            b_color) != 0 or cv2.countNonZero(g_color) != 0 or cv2.countNonZero(r_color) != 0