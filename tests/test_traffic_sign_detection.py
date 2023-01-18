"""Importing needed libraries"""
import pytest
import cv2
from computer_vision.traffic_sign_detection.src.main import TrafficSignDetector
PATH = "computer_vision/traffic_sign_detection/images/test"

cases_ok = [
    ('1.jpg', 1),
    ('2.jpg', 10),
    ('road422.png', 0)
]

cases_not_ok = [('1.jpg', 0),
    ('2.jpg', 12),
    ('road422.png', 1)
]

class TestParametrized:
    """
    DOC: Testing TrafficSignDetection class from module traffic_sign_detection
    """

    def detect_signs(self, source):
        """Initialization the class to test and use it"""
        traffic_sign_detection = TrafficSignDetector()
        image = cv2.imread(f"{PATH}/{source}")
        signs = traffic_sign_detection.detect_signs(image)
        return signs

    @pytest.mark.parametrize('source, expected',cases_ok)
    def test_ok(self, source, expected):
        """Tests where the expected is equal to the output given from the method"""
        signs = self.detect_signs(source)
        assert len(signs) == expected

    @pytest.mark.parametrize('source, expected',cases_not_ok)
    def test_not_ok(self, source, expected):
        """Tests where the expected is not equal to the output given from the method"""
        signs = self.detect_signs(source)
        assert len(signs) != expected