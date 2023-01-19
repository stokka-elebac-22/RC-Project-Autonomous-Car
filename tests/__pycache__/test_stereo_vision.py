"""TEST STEREOSCOPIC VISION"""
import pytest
import cv2 as cv
from  stereoscopic_vision.src.stereoscopic_vision import StereoscopicVision

@pytest.mark.paramterize(
    ["path", "exp"],
    [
        ('DC142', [True, 90]),
        ('DC125', [True, 75]),
        ('DC136', [True, 60]),
        ('DC137', [True, 45]),
        ('DC138', [False, 30]),
        ('DC141', [False, 15]),
    ]
)

def test_(pts, exp):
    """Testing sides"""
    stereo_vision = StereoscopicVision
    stereo_vision.obstacle_detection()
    True, depth_mean, (x_pos, y_pos), (w_rect, h_rect)