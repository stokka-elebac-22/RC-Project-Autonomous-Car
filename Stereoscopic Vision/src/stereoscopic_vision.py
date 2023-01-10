import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

from camera import Camera

class StereoscopicVision:
    def __init__(self, cam1: Camera, cam2: Camera, delay=1) -> None:
        # CAMERAS
        self.cam1 = cam1
        self.cam2 = cam2 

        self.delay = delay

    def run(self):
        while True:
            ret1, frame1 = self.cam1.read()
            ret2, frame2 = self.cam2.read()
            if not ret1 or not ret2:
                continue

            frame1 = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
            frame2 = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
            
            stereo = cv.StereoBM_create(numDisparities=0, blockSize=21)
            disparity = stereo.compute(frame1, frame2)

            plt.imshow(disparity, 'gray')
            plt.show()

            if cv.waitKey(self.delay) & 0xFF == ord('q'):
                break
        cv.destroyWindow(self.window_name)