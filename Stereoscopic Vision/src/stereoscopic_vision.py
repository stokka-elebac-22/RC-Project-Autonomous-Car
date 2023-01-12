import cv2 as cv
import numpy as np
from camera import Camera

# ----- ORIGINAL MEASUREMENTS -----
# QR Code measured, 55mm lense
QR_SIZE_PX = 76
QR_SIZE_MM = 52
QR_DISTANCE = 500


class StereoscopicVision:
    def __init__(self, cam_left: Camera, cam_right: Camera, delay=1, num_disparities=0, block_size=5, min_disparity=5) -> None:
        # CAMERAS
        self.cam_left = cam_left
        self.cam_right = cam_right

        self.num_disparities = num_disparities
        self.block_size = block_size
        self.min_disparity = min_disparity

        self.delay = delay

    def run(self, path="Stereoscopic Vision\data\stereo_rectify_maps.xml"):
        """The path is the path to the calibration paramters (xml file)"""
        stereo_map_left_x, stereo_map_left_y, stereo_map_right_x, stereo_map_right_y = self.read_stereo_map(path)
        stereo = cv.StereoBM_create(numDisparities=self.num_disparities, blockSize=self.block_size)

        cv.namedWindow('disp', cv.WINDOW_NORMAL)
        cv.resizeWindow('disp', 800,600)

        def nothing(x):
            pass

        cv.createTrackbar('numDisparities','disp',1,17, nothing)
        cv.createTrackbar('blockSize','disp',5,50,nothing)
        cv.createTrackbar('preFilterType','disp',1,1,nothing)
        cv.createTrackbar('preFilterSize','disp',2,25,nothing)
        cv.createTrackbar('preFilterCap','disp',5,62,nothing)
        cv.createTrackbar('textureThreshold','disp',10,100,nothing)
        cv.createTrackbar('uniquenessRatio','disp',15,100,nothing)
        cv.createTrackbar('speckleRange','disp',0,100,nothing)
        cv.createTrackbar('speckleWindowSize','disp',3,25,nothing)
        cv.createTrackbar('disp12MaxDiff','disp',5,25,nothing)
        cv.createTrackbar('minDisparity','disp',5,25,nothing)

        while True:
            ret_left, frame_left = self.cam_left.read()
            ret_right, frame_right = self.cam_right.read()

            if ret_left and ret_right:
                gray_left = cv.cvtColor(frame_left, cv.COLOR_BGR2GRAY)
                gray_right = cv.cvtColor(frame_right, cv.COLOR_BGR2GRAY)

                # Applying stereo image rectification on the left image
                rect_left = cv.remap(gray_left, stereo_map_left_x, stereo_map_left_y, cv.INTER_LANCZOS4, cv.BORDER_CONSTANT, 0)
                # Applying stereo image rectification on the right image
                rect_right = cv.remap(gray_right, stereo_map_right_x, stereo_map_right_y, cv.INTER_LANCZOS4, cv.BORDER_CONSTANT, 0)

                # cv.imshow('left', rect_left)
                # cv.imshow('right', rect_right)

                # Updating the parameters based on the trackbar positions
                numDisparities = cv.getTrackbarPos('numDisparities','disp')*16 + 16 # just so you do not make it 0 and program crashes
                blockSize = cv.getTrackbarPos('blockSize','disp')*2 + 5
                preFilterType = cv.getTrackbarPos('preFilterType','disp')
                preFilterSize = cv.getTrackbarPos('preFilterSize','disp')*2 + 5
                preFilterCap = cv.getTrackbarPos('preFilterCap','disp')
                textureThreshold = cv.getTrackbarPos('textureThreshold','disp')
                uniquenessRatio = cv.getTrackbarPos('uniquenessRatio','disp')
                speckleRange = cv.getTrackbarPos('speckleRange','disp')
                speckleWindowSize = cv.getTrackbarPos('speckleWindowSize','disp')*2
                disp12MaxDiff = cv.getTrackbarPos('disp12MaxDiff','disp')
                minDisparity = cv.getTrackbarPos('minDisparity','disp')

                # Setting the updated parameters before computing disparity map
                stereo.setNumDisparities(numDisparities)
                stereo.setBlockSize(blockSize)
                stereo.setPreFilterType(preFilterType)
                stereo.setPreFilterSize(preFilterSize)
                stereo.setPreFilterCap(preFilterCap)
                stereo.setTextureThreshold(textureThreshold)
                stereo.setUniquenessRatio(uniquenessRatio)
                stereo.setSpeckleRange(speckleRange)
                stereo.setSpeckleWindowSize(speckleWindowSize)
                stereo.setDisp12MaxDiff(disp12MaxDiff)
                stereo.setMinDisparity(minDisparity)

                disparity = stereo.compute(rect_left, rect_right)
                """
                NOTE: Code returns a 16bit signed single channel image (CV_16S), containing a disparity map scaled by 16.
                Hence it is essential to convert it to CV_32F and scale it down 16 times.
                """

                # Converting to float32
                disparity = disparity.astype(np.float32)

                # Scaling down the disparity values and normalizing them
                disparity = (disparity/16.0 - minDisparity)/numDisparities

                # Displaying the disparity
                cv.imshow('disparity', disparity)

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

if "__main__" == __name__:
    '''
    NOTE: if you also have a webcam (that you do not want to use), use id 0 and 2 (not always the case....)
    '''
    cam_left = Camera(camera_id=0, window_name='Left camera')
    cam_right = Camera(camera_id=1, window_name='Right camera')
    stereo_vision = StereoscopicVision(cam_left, cam_right)
    stereo_vision.run()