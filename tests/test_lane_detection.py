"""Importing needed libraries"""
import pytest
import cv2
from computer_vision.lane_detection.main import LaneDetector
PATH = "computer_vision/lane_detection/assets/"

sources = ['bike_park.jpg']


class TestParametrized:
    """
    DOC: Testing TrafficSignDetection class from module traffic_sign_detection
    """

    def get_image(self, source):
        """Helping function for tests to get a cv2 image from a source file"""
        image = cv2.imread(PATH + source)
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

    # @pytest.mark.parametrize('source, expected',cases_ok)
    @pytest.mark.skip(reason="no way of currently testing this")
    def test_get_line_coordinates_from_parameters(self, source, expected):
        """Test if the returned values are equal to the manual calculated values"""
        lane_detector = LaneDetector()
        image = self.get_image(source)
        coordinates = lane_detector.get_line_coordinates_from_parameters(image, [
                                                                         2, 3])
        assert coordinates[0] == expected[0]
        assert coordinates[1] == expected[1]
        assert coordinates[2] == expected[2]
        assert coordinates[3] == expected[3]

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_get_average_lines(self, source, lines, expected):
        "Test if the returned lines are equal to the manual calculated values"
        lane_detector = LaneDetector()
        image = self.get_image(source)
        avg_lines = lane_detector.get_average_lines(image, lines)
        assert avg_lines[0] == expected[0] or avg_lines[0] == expected[1]
        assert avg_lines[1] == expected[1] or avg_lines[1] == expected[0]
        assert avg_lines[0] != avg_lines[1]

    @pytest.mark.parametrize('source', sources)
    def test_get_lane_lines(self, source):
        """Test if method returns lane lines when there are lane lines"""
        lane_detector = LaneDetector()
        image = self.get_image(source)
        lines = lane_detector.get_lane_lines(image)
        assert len(lines) > 0

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_get_diff_from_center_info(self, source, lines, expected):
        """Test if the output value is equal to the manual calculation value"""
        lane_detector = LaneDetector()
        image = self.get_image(source)
        diff = lane_detector.get_diff_from_center_info(image, lines)
        assert diff == expected

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_get_course(self, source, points, expected):
        """Test if the output value is equal to the manual calculation value"""
        lane_detector = LaneDetector()
        image = self.get_image(source)
        shape, perspective_transform, coordinates, polys = lane_detector.get_course(
            image, points)
        assert shape == expected[0]
        assert perspective_transform == expected[1]
        assert coordinates == expected[2]
        assert polys == expected[3]
