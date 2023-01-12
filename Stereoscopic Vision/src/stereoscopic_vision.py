import cv2 as cv

from camera import Camera

class StereoscopicVision:
    def __init__(self, cam1: Camera, cam2: Camera, delay=1, num_disparities=0, block_size=21) -> None:
        # CAMERAS
        self.cam1 = cam1
        self.cam2 = cam2

        self.num_disparities = num_disparities
        self.block_size = block_size

        self.delay = delay

    def run(self):
        while True:
            ret1, frame1 = self.cam1.read()
            ret2, frame2 = self.cam2.read()
            if not ret1 or not ret2:
                continue

            disparity = self.disparity(frame1, frame2)
            cv.imshow('gray', disparity)

            if cv.waitKey(self.delay) & 0xFF == ord('q'):
                break
        cv.destroyWindow(self.window_name)

    def read_stereo_map(self, path):
        cv_file = cv.FileStorage(path, cv.FILE_STORAGE_READ)
        stereo_map_left_x = cv_file.getNode("stereo_map_left_x").mat()
        stereo_map_left_y = cv_file.getNode("stereo_map_left_y").mat()
        stereo_map_right_x = cv_file.getNode("stereo_map_right_x").mat()
        stereo_map_right_y = cv_file.getNode("stereo_map_right_y").mat()
        cv_file.release()
        return stereo_map_left_x, stereo_map_left_y, stereo_map_right_x, stereo_map_right_y

    def disparity(self, frame1, frame2):
        frame1 = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
        frame2 = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)

        stereo = cv.StereoBM_create(numDisparities=self.num_disparities, blockSize=self.block_size)
        disparity = stereo.compute(frame1, frame2)
        return disparity
