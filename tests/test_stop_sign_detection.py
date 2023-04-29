'''Importing needed libraries'''
import pytest
import cv2
from computer_vision.stop_sign_detection.stop_sign_detector import StopSignDetector
PATH = 'tests/images/stop_sign'

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
    '''
    DOC: Testing StopSignDetection class from module stop_sign_detection
    '''

    def detect_signs(self, source):
        '''Initialization the class to test and use it'''
        stop_sign_detection = StopSignDetector()
        image = cv2.imread(f'{PATH}/{source}')
        signs = stop_sign_detection.detect_signs(image)
        return signs

    @pytest.mark.parametrize('source, expected',cases_ok)
    def test_ok(self, source, expected):
        '''Tests where the expected is equal to the output given from the method'''
        signs = self.detect_signs(source)
        assert len(signs) == expected

    @pytest.mark.parametrize('source, expected',cases_not_ok)
    def test_not_ok(self, source, expected):
        '''Tests where the expected is not equal to the output given from the method'''
        signs = self.detect_signs(source)
        assert len(signs) != expected
