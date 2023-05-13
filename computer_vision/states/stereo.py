
import cv2
from stereoscopic_vision.src.stereoscopic_vision import StereoscopicVision

class StereoAction():
    '''Class for waiting state'''
    def __init__(self, conf) -> None:
        self.conf = conf
        self.stereo_vision = StereoscopicVision(
            conf['stereo']['maps_path'],
            conf['stereo']['parameter_path'])

    def run_calculation(self, input_data):
        '''Take frame input and output relevant data'''
        frame0 = cv2.blur(input_data[0], (self.conf['stereo']['blur']))
        frame1 = cv2.blur(input_data[1], (self.conf['stereo']['blur']))
        current_disparity = self.stereo_vision.get_disparity(
                        frame0, frame1)
        ret_val, depth_val, pos_val, size_val = self.stereo_vision.get_data(
            current_disparity,
            self.conf['stereo']['min_dist'],
            self.conf['stereo']['max_dist']
        )
        return depth_val
