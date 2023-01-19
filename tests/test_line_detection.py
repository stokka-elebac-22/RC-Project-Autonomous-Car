"""Importing needed libraries"""
import pytest
import cv2
import numpy as np
from computer_vision.line_detection.main import LineDetector
PATH = "computer_vision/line_detection/assets/"


class TestParametrized:
    """
    DOC: Testing LineDetection class from module line_detection
    """

    def get_image(self, source):
        """Helping function for tests to get a cv2 image from a source file"""
        image = cv2.imread(PATH + source)
        return image

    @pytest.mark.parametrize('img_source', ['bike_park.jpg', 'curve.jpg', '1.jpg', '2.jpg'])
    def test_get_region_of_interest(self, img_source):
        """Test if the output image is equal to the input image"""
        line_detector = LineDetector()
        original_image = self.get_image(img_source)

        new_image = line_detector.get_region_of_interest(original_image)
        difference = cv2.subtract(original_image, new_image)
        b_color, g_color, r_color = cv2.split(difference)
        assert new_image.shape == original_image.shape and cv2.countNonZero(
            b_color) == 0 and cv2.countNonZero(g_color) == 0 and cv2.countNonZero(r_color) == 0

    @pytest.mark.parametrize('img_source, line, expected', [
        ('bike_park.jpg', [-0.8819273, 822.19240925],
         [-2469, 3000, -632, 1380]),
        ('curve.jpg', [-0.123, 423.], [-20951, 3000, -7780, 1380]),
        ('1.jpg', [1.881, -0.493], [1595, 3000, 733, 1380]),
        ('2.jpg', [2.34, 423.1924], [1101, 3000, 408, 1380])])
    def test_get_line_coordinates_from_parameters(self, img_source, line, expected):
        '''Test if the output coordinates are equal to the expected coordinates'''
        line_detector = LineDetector()
        image = self.get_image(img_source)

        coordinates = line_detector.get_line_coordinates_from_parameters(
            image, line)

        assert coordinates[0] == expected[0]
        assert coordinates[1] == expected[1]
        assert coordinates[2] == expected[2]
        assert coordinates[3] == expected[3]

    @pytest.mark.parametrize('img_source, expected', [
        ('bike_park.jpg', 3852),
        ('curve.jpg', 4292),
        ('1.jpg', 1921),
        ('2.jpg', 2569)])
    def test_get_lines(self, img_source, expected):
        '''Test if the output lines length is equal to the expected length'''
        line_detector = LineDetector()
        image = self.get_image(img_source)
        lines = line_detector.get_lines(image)
        assert len(lines) == expected

    @pytest.mark.parametrize('img_source, lines', [
        ('bike_park.jpg', [np.array([-249, 100, 532, 180])]),
        ('curve.jpg', [np.array([-100, 200, 300, 130])]),
        ('1.jpg', [np.array([123, 300, 733, 1380])]),
        ('2.jpg', [np.array([1101, 3000, 408, 1380])])])
    def test_show_lines(self, img_source, lines):
        """Test if the output image is not equal to the input image"""
        line_detector = LineDetector()
        original_image = self.get_image(img_source)
        copy_image = original_image.copy()

        line_detector.show_lines(copy_image, lines)
        difference = cv2.subtract(original_image, copy_image)
        b_color, g_color, r_color = cv2.split(difference)
        assert copy_image.shape != original_image.shape or cv2.countNonZero(
            b_color) != 0 or cv2.countNonZero(g_color) != 0 or cv2.countNonZero(r_color) != 0
