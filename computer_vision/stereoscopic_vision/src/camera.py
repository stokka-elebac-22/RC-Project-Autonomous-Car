'''Camera'''
import cv2 as cv
class Camera: # pylint: disable=R0903
    '''Camera'''
    def __init__(self, camera_id=0, window_name='window'):
        self.camera_id = camera_id
        self.window_name = window_name
        self.cap = cv.VideoCapture(self.camera_id)

    def read(self):
        '''Read'''
        ret, frame = self.cap.read()
        return ret, frame
        