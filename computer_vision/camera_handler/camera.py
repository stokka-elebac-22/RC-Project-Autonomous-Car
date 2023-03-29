'''Camera'''
from sys import platform
from typing import Tuple
import cv2 as cv

class Camera: # pylint: disable=R0903
    '''Camera'''
    def __init__(self, camera_id=0, window_name='window', resolution: Tuple[int, int] = None):
        '''
        Init the camera
        resolution is optional ([width, height])
        '''
        self.camera_id = camera_id
        self.window_name = window_name
        if platform in ['linux', 'linux2', 'darwin']:
            # linux or OSX
            self.cap = cv.VideoCapture(self.camera_id)
            self.cap.set(cv.CAP_PROP_AUTOFOCUS, 0) # turn autofocus off
        elif platform == 'win32':
            # windows
            self.cap = cv.VideoCapture(self.camera_id, cv.CAP_DSHOW)
            self.cap.set(cv.CAP_PROP_AUTOFOCUS, 0) # turn autofocus off
            if resolution is not None:
                self.cap.set(cv.CAP_PROP_FRAME_WIDTH, resolution[0])
                self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, resolution[1])

    def read(self):
        '''Read'''
        ret, frame = self.cap.read()
        return ret, frame

    def get_dimensions(self) -> Tuple[float, float]:
        '''Returns width and height'''
        width  = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)   # float `width`
        height = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)  # float `height`
        return width, height
