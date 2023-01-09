import cv2 as cv

from camera import Camera

class StereoscopicVision:
    def __init__(self, cam1: Camera, cam2: Camera, delay=1) -> None:
        # CAMERAS
        self.cam1 = cam1
        self.cam2 = cam2 

        self.delay = 1

    def run(self):
        while True:
            self.cam1.show() 
            self.cam2.show()
            if cv.waitKey(self.delay) & 0xFF == ord('q'):
                break
        cv.destroyWindow(self.window_name)