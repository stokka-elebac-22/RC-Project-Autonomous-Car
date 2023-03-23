'''Camera'''
import cv2 as cv

class Camera:
    '''Camera'''
    def __init__(self, camera_id=0, delay=1, window_name='window'):
        self.camera_id = camera_id
        self.delay = delay
        self.window_name = window_name
        self.cap = cv.VideoCapture(self.camera_id)

    def read(self, name=None, resize=1):
        '''Read'''
        if not name:
            ret, frame = self.cap.read()
            return ret, frame
        frame = cv.imread(name)
        frame = cv.resize(frame, (0, 0), fx = resize, fy = resize)
        return True, frame
