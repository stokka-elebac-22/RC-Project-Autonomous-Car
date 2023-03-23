'''Camera'''
import cv2 as cv

class Camera:
    '''Camera'''
    def __init__(self, camera_id=0, delay=1, window_name='window'):
        self.camera_id = camera_id
        self.delay = delay
        self.window_name = window_name
        self.cap = cv.VideoCapture(self.camera_id)

    def run(self, name=None, resize=1, verbose=1):
        '''Run'''
        if not name:
            self.run_video(verbose)
        else:
            self.run_image(name, resize, verbose)

    def run_video(self, verbose=1):
        '''Run video'''
        while True:
            frame = self.read()
            self.detect_qr_code(frame, verbose=verbose)
            cv.imshow(self.window_name, frame)
            if cv.waitKey(self.delay) & 0xFF == ord('q'):
                break
        cv.destroyWindow(self.window_name)

    def read(self, name=None, resize=1):
        '''Read'''
        if not name:
            ret, frame = self.cap.read()
            return ret, frame
        frame = cv.imread(name)
        frame = cv.resize(frame, (0, 0), fx = resize, fy = resize)
        return True, frame
