"""Importing needed libraries"""
import pytest
import cv2
import numpy as np
from computer_vision.line_detection.lane_detector import LineDetector
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

    @pytest.mark.parametrize('img_source, expected', [
        ('bike_park.jpg', 3413),
        ('curve.jpg', 3619),
        ('1.jpg', 1789),
        ('2.jpg', 2570)])
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
