'''Camera'''
from sys import platform
import cv2 as cv

class Camera: # pylint: disable=R0903
    '''Camera'''
    def __init__(self, camera_id=0, window_name='window'):
        self.camera_id = camera_id
        self.window_name = window_name
        if platform == 'linux' or platform == 'linux2' or platform == 'darwin':
            # linux or OSX
            self.cap = cv.VideoCapture(self.camera_id)
            self.cap.set(cv.CAP_PROP_AUTOFOCUS, 0) # turn the autofocus off
        elif platform == 'win32':
            # Windows...
            self.cap = cv.VideoCapture(self.camera_id, cv.CAP_DSHOW)
            self.cap.set(cv.CAP_PROP_AUTOFOCUS, 0) # turn the autofocus off
            self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
            self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

    def read(self):
        '''Read'''
        ret, frame = self.cap.read()
        return ret, frame
