"""Importing needed libraries"""
import pytest
import cv2
import numpy as np
from computer_vision.lane_detection.main import LaneDetector
PATH = "computer_vision/lane_detection/assets/"

sources = ['bike_park.jpg']
sources_lines_coordinates = [(sources[0],
    [-0.8819273, 822.19240925],
    [-2469, 3000, -768, 1500]
)]

sources_lines_avg = [(
    sources[0],
    [
        np.array([2407, 2273, 2650, 2234]),
        np.array([328, 2530, 1111, 2433]),
        np.array([593, 2807, 945, 2757]),
        np.array([ 429,2512 ,673,2529]),
        np.array([ 683,2411,937,2447]),
        np.array([ 345,2517,580,2541])
    ],
    [
        np.array([-2060,  3000,  8492,  1500]),
        np.array([ 5492,  3000, -8860,  1500])
    ]
)]
sources_lines_diffs = [(
    sources[0],
    sources_lines_avg[0][2],
    14.2
)]
sources_for_course = [(
    sources[0],
    sources_lines_avg[0][2],
    (3000, 7552, 3)
)]
class TestParametrized:
    """
    DOC: Testing TrafficSignDetection class from module traffic_sign_detection
    """

    def get_image(self, source):
        """Helping function for tests to get a cv2 image from a source file"""
        image = cv2.imread(PATH + source)
        SCALE_PERCENT = 100  # percent of original size
        new_width = int(image.shape[1] * SCALE_PERCENT / 100)
        new_height = int(image.shape[0] * SCALE_PERCENT / 100)
        dim = (new_width, new_height)
        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        return image

    @pytest.mark.parametrize('source', sources)
    def test_get_lane_region(self, source):
        """Test if the output image is not equal to the input image"""
        lane_detector = LaneDetector()
        original_image = self.get_image(source)

        new_image = lane_detector.get_lane_region(original_image)
        difference = cv2.subtract(original_image, new_image)
        b, g, r = cv2.split(difference)
        assert new_image.shape != original_image.shape or cv2.countNonZero(
            b) != 0 or cv2.countNonZero(g) != 0 or cv2.countNonZero(r) != 0

    @pytest.mark.parametrize('source, line, expected', sources_lines_coordinates)
    def test_get_line_coordinates_from_parameters(self, source, line, expected):
        """Test if the returned values are equal to the manual calculated values"""
        lane_detector = LaneDetector()
        image = self.get_image(source)
        coordinates = lane_detector.get_line_coordinates_from_parameters(
            image, line)
        coordinates = np.sort(coordinates)
        expected = np.sort(expected)
        assert coordinates[0] == expected[0]
        assert coordinates[1] == expected[1]
        assert coordinates[2] == expected[2]
        assert coordinates[3] == expected[3]

    @pytest.mark.parametrize('source, lines, expected', sources_lines_avg)
    def test_get_average_lines(self, source, lines, expected):
        "Test if the returned lines are equal to the manual calculated values"
        lane_detector = LaneDetector()
        image = self.get_image(source)
        avg_lines = lane_detector.get_average_lines(image, lines)
        assert (avg_lines[0] == expected[0]).all() or (avg_lines[0] == expected[1]).all()
        assert (avg_lines[1] == expected[1]).all() or (avg_lines[1] == expected[0]).all()
        assert (avg_lines[0] != avg_lines[1]).any()

    @pytest.mark.parametrize('source', sources)
    def test_get_lane_lines(self, source):
        """Test if method returns lane lines when there are lane lines"""
        lane_detector = LaneDetector()
        image = self.get_image(source)
        lines = lane_detector.get_lane_lines(image)
        assert len(lines) > 0

    @pytest.mark.parametrize('source, lines, expected', sources_lines_diffs)
    def test_get_diff_from_center_info(self, source, lines, expected):
        """Test if the output value is equal to the manual calculation value"""
        lane_detector = LaneDetector()
        image = self.get_image(source)
        diff = lane_detector.get_diff_from_center_info(image, lines)
        assert diff == expected

    @pytest.mark.parametrize('source, lines, shape', sources_for_course)
    def test_get_course(self, source, lines, shape):
        """Test if the output value is equal to the manual calculation value"""
        lane_detector = LaneDetector()
        image = self.get_image(source)
        output_shape, _, coordinates, _ = lane_detector.get_course(
            image, lines)
        assert output_shape == shape
        assert len(coordinates) == 3