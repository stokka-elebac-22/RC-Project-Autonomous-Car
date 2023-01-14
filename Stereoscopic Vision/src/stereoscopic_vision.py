"""Importing necessary libraries"""
import cv2 as cv
import numpy as np
from camera import Camera

# ----- ORIGINAL MEASUREMENTS -----
# QR Code measured, 55mm lense
QR_SIZE_PX = 76
QR_SIZE_MM = 52
QR_DISTANCE = 500


class StereoscopicVision:
    """
    DOC:
    """
    def __init__(self, path="", num_disp=0, block_size=5, min_disp=5) -> None:
        self.num_disp = num_disp
        self.block_size = block_size
        self.min_disp = min_disp

        # The path is the path to the calibration paramters (xml file)
        self.stereo_map_left, self.stereo_map_right = self.read_stereo_map(path)
        self.stereo = cv.StereoBM_create(numDisparities=self.num_disp, blockSize=self.block_size)

    def get_disparity(self, image_left, image_right):
        """Calculates and return the disparity"""
        gray_left = cv.cvtColor(image_left, cv.COLOR_BGR2GRAY)
        gray_right = cv.cvtColor(image_right, cv.COLOR_BGR2GRAY)

        # Applying stereo image rectification on the left image
        rect_left = cv.remap(
            gray_left,
            self.stereo_map_left[0],
            self.stereo_map_left[1],
            cv.INTER_LANCZOS4,
            cv.BORDER_CONSTANT,
            0)
        # Applying stereo image rectification on the right image
        rect_right = cv.remap(
            gray_right,
            self.stereo_map_right[0],
            self.stereo_map_right[1],
            cv.INTER_LANCZOS4,
            cv.BORDER_CONSTANT,
            0)

        disparity = self.stereo.compute(rect_left, rect_right)
        # NOTE: Code returns a 16bit signed single channel image (CV_16S),
        # containing a disparity map scaled by 16.
        # Hence it is essential to convert it to CV_32F and scale it down 16 times.

        # Converting to float32
        disparity = disparity.astype(np.float32)

        # Scaling down the disparity values and normalizing them
        disparity = (disparity/16.0 - self.min_disp)/self.num_disp

        return disparity

    def read_stereo_map(self, path):
        """Reading from stereo map xml file"""
        cv_file = cv.FileStorage(path, cv.FILE_STORAGE_READ)
        stereo_map_left_x = cv_file.getNode("stereo_map_left_x").mat()
        stereo_map_left_y = cv_file.getNode("stereo_map_left_y").mat()
        stereo_map_right_x = cv_file.getNode("stereo_map_right_x").mat()
        stereo_map_right_y = cv_file.getNode("stereo_map_right_y").mat()
        cv_file.release()
        return (stereo_map_left_x, stereo_map_left_y), (stereo_map_right_x, stereo_map_right_y)

    def obstacle_detection(self, frame):
        """Detecting depth to obstacles in cm"""
        # Mask to segment regions with depth less than threshold
        mask = cv.inRange(depth_map, 10, DEPTH_THRESH)

        # Check if a significantly large obstacle is present and filter out smalle noisy regions
        if np.sum(mask)/255.0 > 0.01*mask.shape[0]*mask.shape[1]:
            # Contour detection
            contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            cnts = sorted(contours, key=cv.contourArea, reverse=True)

            # Check if detected contour is significantly large (to avoid multiple tiny regions)
            if cv.contourArea(cnts[0]) > 0.01*mask.shape[0]*mask.shape[1]:
                x_pos, y_pos, w_rect, h_rect = cv.boundingRect(cnts[0])

                # finding average depth of region represented by the largest contour

                mask2 = np.zeros_like(mask)
                cv.drawContours(mask2, cnts, 0, (255), -1)

                # Calculating the average depth of the object closer than the safe distance
                depth_mean, _ = cv.meanStdDev(depth_map, mask=mask2)

                # Display warning text
                cv.putText(frame, f"{depth_mean} cm", (x_pos+5, y_pos+40), 1, 2, (100, 10, 25), 2, 2)

def nothing(_):
    """Empty function"""

if "__main__" == __name__:
    # NOTE: if you also have a webcam (that you do not want to use),
    # use id 0 and 2 (not always the case....)
    cam_left = Camera(camera_id=0, window_name='Left camera')
    cam_right = Camera(camera_id=1, window_name='Right camera')
    stereo_vision = StereoscopicVision(path="Stereoscopic Vision/data/stereo_rectify_maps.xml")

    cv.namedWindow('disp', cv.WINDOW_NORMAL)
    cv.resizeWindow('disp', 800,600)

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

    # This measurements needs to be calculated from the setup
    MAX_DIST = 230.0 # max distance to keep the target object (in cm)
    MIN_DIST = 30.0 # min distance to keep the target object (in cm)
    DEPTH_THRESH = 50.0 # Threshold for safe distance (in cm)

    M = 39.075
    Z = MAX_DIST
    value_pairs = []

    while True:
        ret_left, frame_left = cam_left.read()
        ret_right, frame_right = cam_right.read()
        if ret_left and ret_right:
            disp = stereo_vision.get_disparity(frame_left, frame_right)
            # Displaying the disparity
            # Updating the parameters based on the trackbar positions
            numDisparities = cv.getTrackbarPos('numDisparities','disp')*16 + 16
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
            stereo_vision.stereo.setNumDisparities(numDisparities)
            stereo_vision.stereo.setBlockSize(blockSize)
            stereo_vision.stereo.setPreFilterType(preFilterType)
            stereo_vision.stereo.setPreFilterSize(preFilterSize)
            stereo_vision.stereo.setPreFilterCap(preFilterCap)
            stereo_vision.stereo.setTextureThreshold(textureThreshold)
            stereo_vision.stereo.setUniquenessRatio(uniquenessRatio)
            stereo_vision.stereo.setSpeckleRange(speckleRange)
            stereo_vision.stereo.setSpeckleWindowSize(speckleWindowSize)
            stereo_vision.stereo.setDisp12MaxDiff(disp12MaxDiff)
            stereo_vision.stereo.setMinDisparity(minDisparity)

            stereo_vision.num_disp = numDisparities
            stereo_vision.min_disp = minDisparity

            depth_map = M/disp # for depth in cm

            mask_tmp = cv.inRange(depth_map, MIN_DIST, MAX_DIST)
            depth_map = cv.bitwise_and(depth_map, depth_map, mask=mask_tmp)

            stereo_vision.obstacle_detection(frame_left)

            cv.imshow('frame left', frame_left)
            cv.imshow('disparity', disp)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

    cv.destroyWindow(stereo_vision.window_name)
