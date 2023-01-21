'''TEST'''
import pytest
import cv2 as cv
from computer_vision.stereoscopic_vision.src.stereoscopic_vision import StereoscopicVision

@pytest.mark.parametrize(
    ['name', 'exp'],
    [
        [('left_32', 'right_32'), True],
        [('left_40', 'right_40'), True],
        [('left_100', 'right_100'), True],
        [('left_200', 'right_200'), True],
    ]
)
def test_get_disparity(name, exp):
    '''Test get disparity'''
    stereo_vision = StereoscopicVision()
    left_path = f'tests/images/stereoscopic_vision/distance/logi_1080p/left/{name[0]}'
    right_path = f'tests/images/stereoscopic_vision/distance/logi_1080p/right/{name[1]}'

    left_img = cv.imread(left_path)
    right_img = cv.imread(right_path)

    disparity = stereo_vision.get_disparity(left_img, right_img)
    assert disparity == exp

@pytest.mark.parametrize(
    ['name', 'exp'],
    [
        [('left_32', 'right_32'), (True, 320)],
        [('left_40', 'right_40'), (True, 400)],
        [('left_51', 'right_51'), (True, 510)],
        [('left_60', 'right_60'), (True, 600)],
        [('left_80', 'right_80'), (True, 800)],
        [('left_82', 'right_82'), (True, 820)],
        [('left_100', 'right_100'), (True, 1000)],
        [('left_140', 'right_140'), (True, 1400)],
        [('left_142', 'right_142'), (True, 1420)],
        [('left_200', 'right_200'), (True, 2000)],
        [('left_250', 'right_250'), (True, 2500)],
        [('left_300', 'right_300'), (True, 3000)],
    ]
)
def test_get_data(name, exp):
    '''Test get data'''
    stereo_vision = StereoscopicVision()
    left_path = f'tests/images/stereoscopic_vision/distance/logi_1080p/left/{name[0]}'
    right_path = f'tests/images/stereoscopic_vision/distance/logi_1080p/right/{name[1]}'
    left_img = cv.imread(left_path)
    right_img = cv.imread(right_path)
    disparity = stereo_vision.get_disparity(left_img, right_img)
    retval, depth, _, _ = stereo_vision.get_data(disparity)
    assert retval == exp[0] and depth == pytest.approx(exp[1])

