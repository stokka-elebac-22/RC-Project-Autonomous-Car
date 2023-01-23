'''Test stereo vision'''
import pytest
import cv2 as cv
from computer_vision.stereoscopic_vision.src.stereoscopic_vision import StereoscopicVision

class TestStereoVision:
    '''Class for testing stereo vision'''
    @pytest.mark.parametrize(
        ['name'],
        [
            [('left_32', 'right_32')],
            [('left_40', 'right_40')],
            [('left_100', 'right_100')],
            [('left_200', 'right_200')],
        ]
    )
    @pytest.mark.skip(reason='No way of testing atm')
    def test_get_disparity(self, name):
        '''Test get disparity'''
        stereo_rectify_maps_path = \
            'computer_vision/stereoscopic_vision/data/stereo_rectify_maps.xml'
        stereo_parameter_path = 'computer_vision/stereoscopic_vision/data/stereo_parameters.xml'
        stereo_vision = StereoscopicVision(stereo_rectify_maps_path, stereo_parameter_path)
        left_path = f'tests/images/stereoscopic_vision/distance/logi_1080p/left/{name[0]}.jpg'
        right_path = f'tests/images/stereoscopic_vision/distance/logi_1080p/right/{name[1]}.jpg'

        left_img = cv.imread(left_path)
        right_img = cv.imread(right_path)

        disparity = stereo_vision.get_disparity(left_img, right_img)
        assert disparity is not None

    @pytest.mark.parametrize(
        ['name', 'exp'],
        [
            [('left_32', 'right_32'), (True, 320)],
            # [('left_40', 'right_40'), (True, 400)],
            # [('left_51', 'right_51'), (True, 510)],
            # [('left_60', 'right_60'), (True, 600)],
            # [('left_80', 'right_80'), (True, 800)],
            # [('left_82', 'right_82'), (True, 820)],
            # [('left_100', 'right_100'), (True, 1000)],
            # [('left_140', 'right_140'), (True, 1400)],
            # [('left_142', 'right_142'), (True, 1420)],
            # [('left_200', 'right_200'), (True, 2000)],
            # [('left_250', 'right_250'), (True, 2500)],
            # [('left_300', 'right_300'), (True, 3000)],
        ]
    )
    @pytest.mark.skip(reason='No way of testing atm')
    def test_get_data(self, name, exp):
        '''Test get data'''
        max_dist = 230.0 # max distance to recognize objects (cm)
        min_dist = 1.0 # min distance to recognize objects (cm)
        thresh_dist = max_dist
        stereo_rectify_maps_path = \
            'computer_vision/stereoscopic_vision/data/stereo_rectify_maps.xml'
        stereo_parameter_path = 'computer_vision/stereoscopic_vision/data/stereo_parameters.xml'
        stereo_vision = StereoscopicVision(stereo_rectify_maps_path, stereo_parameter_path)
        left_path = f'tests/images/stereoscopic_vision/distance/logi_1080p/left/{name[0]}.jpg'
        right_path = f'tests/images/stereoscopic_vision/distance/logi_1080p/right/{name[1]}.jpg'
        left_img = cv.imread(left_path)
        right_img = cv.imread(right_path)
        disparity = stereo_vision.get_disparity(left_img, right_img)
        retval, depth, _, _ = stereo_vision.get_data(disparity, min_dist, max_dist, thresh_dist)
        assert retval == exp[0] and depth == pytest.approx(exp[1])
