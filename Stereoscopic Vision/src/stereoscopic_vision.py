"""Importing necessary libraries"""
import os.path
import cv2 as cv
import numpy as np
from camera import Camera

class StereoscopicVision:
    """
    DOC:
    """
    def __init__(self, path="", num_disp=16, block_size=5, min_disp=5) -> None:
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

    def obstacle_detection(self, depth_map, obstacle_area, contour_area):
        """Detecting depth to obstacles in cm"""
        # Mask to segment regions with depth less than threshold
        mask = cv.inRange(depth_map, MIN_DIST, THRES_DIST)

        # Check if a significantly large obstacle is present and filter out smalle noisy regions
        if np.sum(mask)/255.0 > obstacle_area*mask.shape[0]*mask.shape[1]:
            # Contour detection
            contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            cnts = sorted(contours, key=cv.contourArea, reverse=True)

            # Check if detected contour is significantly large (to avoid multiple tiny regions)
            if cv.contourArea(cnts[0]) > contour_area*mask.shape[0]*mask.shape[1]:
                x_pos, y_pos, w_rect, h_rect = cv.boundingRect(cnts[0])
                x_pos, y_pos, w_rect, h_rect = cv.boundingRect(cnts[0])

                # finding average depth of region represented by the largest contour

                mask2 = np.zeros_like(mask)
                cv.drawContours(mask2, cnts, 0, (255), -1)

                # Calculating the average depth of the object closer than the safe distance
                depth_mean, _ = cv.meanStdDev(depth_map, mask=mask2)

                return True, depth_mean, (x_pos, y_pos), (w_rect, h_rect)
        return False, None, None, None

if __name__ == '__main__':
    DESTINATION_PATH = 'Stereoscopic Vision/data/stereo_parameters.xml'
    MAX_DIST = 230.0 # max distance to recognize objects (cm)
    MIN_DIST = 5.0 # min distance to recognize objects (cm)
    THRES_DIST = MAX_DIST
    M = 40 # base value, the real one is from the xml file (and is calculated in a previous test)
    Z = MAX_DIST # The depth, for used for calculating M

    # NOTE: if you also have a webcam (that you do not want to use),
    # use id 0 and 2 (not always the case....)
    cam_left = Camera(camera_id=0, window_name='Left camera')
    cam_right = Camera(camera_id=1, window_name='Right camera')
    stereo_vision = StereoscopicVision(path="Stereoscopic Vision/data/stereo_rectify_maps.xml")

    cv.namedWindow('disp', cv.WINDOW_NORMAL)
    cv.resizeWindow('disp', 800,600)

    def nothing(_):
        """Empty function"""

    # creating trackbars for testing
    cv.createTrackbar('num_disparities','disp',1,17, nothing)
    cv.createTrackbar('block_size','disp',5,50,nothing)
    cv.createTrackbar('pre_filter_type','disp',1,1,nothing)
    cv.createTrackbar('pre_filter_size','disp',2,25,nothing)
    cv.createTrackbar('pre_filter_cap','disp',5,62,nothing)
    cv.createTrackbar('texture_threshold','disp',10,100,nothing)
    cv.createTrackbar('uniqueness_ratio','disp',15,100,nothing)
    cv.createTrackbar('speckle_range','disp',0,100,nothing)
    cv.createTrackbar('speckle_window_size','disp',3,25,nothing)
    cv.createTrackbar('disparity_max_diff','disp',5,25,nothing)
    cv.createTrackbar('min_disparity','disp',5,25,nothing)
    cv.createTrackbar('obstacle_area', 'disp', 1, 100, nothing)
    cv.createTrackbar('contour_area', 'disp', 1, 100, nothing)

    # Getting parameter information from previous tests, if there is one
    if os.path.exists(DESTINATION_PATH):
        cv_file_read = cv.FileStorage(DESTINATION_PATH, cv.FILE_STORAGE_READ)
        cv.setTrackbarPos('num_disparities','disp',
            int(cv_file_read.getNode('num_disparities').real()))
        cv.setTrackbarPos('block_size','disp',
            int(cv_file_read.getNode('block_size').real()))
        cv.setTrackbarPos('pre_filter_type','disp',
            int(cv_file_read.getNode('pre_filter_type').real()))
        cv.setTrackbarPos('pre_filter_size','disp',
            int(cv_file_read.getNode('pre_filter_size').real()))
        cv.setTrackbarPos('pre_filter_cap','disp',
            int(cv_file_read.getNode('pre_filter_cap').real()))
        cv.setTrackbarPos('texture_threshold','disp',
            int(cv_file_read.getNode('texture_threshold').real()))
        cv.setTrackbarPos('uniqueness_ratio','disp',
            int(cv_file_read.getNode('uniqueness_ratio').real()))
        cv.setTrackbarPos('speckle_range','disp',
            int(cv_file_read.getNode('speckle_range').real()))
        cv.setTrackbarPos('speckle_window_size','disp',
            int(cv_file_read.getNode('speckle_window_size').real()))
        cv.setTrackbarPos('disparity_max_diff','disp',
            int(cv_file_read.getNode('disparity_max_diff').real()))
        cv.setTrackbarPos('min_disparity','disp',
            int(cv_file_read.getNode('min_disparity').real()))
        cv.setTrackbarPos('obstacle_area', 'disp',
            int(cv_file_read.getNode('obstacle_area').real()))
        cv.setTrackbarPos('contour_area', 'disp',
            int(cv_file_read.getNode('contour_area').real()))
        M = cv_file_read.getNode('M').real()
        cv_file_read.release()


    value_pairs = [] # used for calculating M (depth ratio)

    while True:
        ret_left, frame_left = cam_left.read()
        ret_right, frame_right = cam_right.read()
        if ret_left and ret_right:
            # NOTE: it might help to blur the image to reduce noise
            # frame_left = cv.blur(frame_left, (10, 10))
            # frame_right = cv.blur(frame_right, (10, 10))
            disp = stereo_vision.get_disparity(frame_left, frame_right)
            # Displaying the disparity
            # Updating the parameters based on the trackbar positions
            num_disparities = cv.getTrackbarPos('num_disparities','disp')*16 + 16
            block_size_disp = cv.getTrackbarPos('block_size','disp')*2 + 5
            pre_filter_type = cv.getTrackbarPos('pre_filter_type','disp')
            pre_filter_size = cv.getTrackbarPos('pre_filter_size','disp')*2 + 5
            pre_filter_cap = cv.getTrackbarPos('pre_filter_cap','disp') + 1
            texture_threshold = cv.getTrackbarPos('texture_threshold','disp')
            uniqueness_ratio = cv.getTrackbarPos('uniqueness_ratio','disp')
            speckle_range = cv.getTrackbarPos('speckle_range','disp')
            speckle_window_size = cv.getTrackbarPos('speckle_window_size','disp')*2
            disparity_max_diff = cv.getTrackbarPos('disparity_max_diff','disp')
            min_disparity = cv.getTrackbarPos('min_disparity','disp')
            #  change how big obstacle area needs to be to be detected
            obs_area = cv.getTrackbarPos('obstacle_area', 'disp') / 1000
            # change how big contour area needs to be to be detected
            cont_area = cv.getTrackbarPos('contour_area', 'disp') / 1000

            # Setting the updated parameters before computing disparity map
            stereo_vision.stereo.setNumDisparities(num_disparities)
            stereo_vision.stereo.setBlockSize(block_size_disp)
            stereo_vision.stereo.setPreFilterType(pre_filter_type)
            stereo_vision.stereo.setPreFilterSize(pre_filter_size)
            stereo_vision.stereo.setPreFilterCap(pre_filter_cap)
            stereo_vision.stereo.setTextureThreshold(texture_threshold)
            stereo_vision.stereo.setUniquenessRatio(uniqueness_ratio)
            stereo_vision.stereo.setSpeckleRange(speckle_range)
            stereo_vision.stereo.setSpeckleWindowSize(speckle_window_size)
            stereo_vision.stereo.setDisp12MaxDiff(disparity_max_diff)
            stereo_vision.stereo.setMinDisparity(min_disparity)

            stereo_vision.num_disp = num_disparities
            stereo_vision.min_disp = min_disparity

            depth_map_dist = M/disp # for depth in cm

            mask_tmp = cv.inRange(depth_map_dist, MIN_DIST, MAX_DIST)
            depth_map_dist = cv.bitwise_and(depth_map_dist, depth_map_dist, mask=mask_tmp)

            retval, depth_mean_obstacle, pos_obstacle, size_obstacle = \
                stereo_vision.obstacle_detection(depth_map_dist, obs_area, cont_area)
            if retval:
                cv.putText(frame_left, f"{depth_mean_obstacle[0][0]} cm",
                    [pos_obstacle[0] + 5, pos_obstacle[1] + 40], 1, 2, (40, 200, 40), 2, 2)

            cv.imshow('frame left', frame_left)
            cv.imshow('disparity', disp)

            if cv.waitKey(1) & 0xFF == ord('q'):
                print('Quitting...')
                break

    cv.destroyWindow('disp')

    # Calculating the disparity list / inverse, solving M and C
    # Value paris should be 2 dimensional
    if len(value_pairs) > 0:
        value_pairs = np.array(value_pairs)
        z = value_pairs[:, 0]
        disp = value_pairs[:,1]
        disp_inv = 1/disp

        # Solving for M using least square fitting with QR decomposition method
        coeff = np.vstack([disp_inv, np.ones(len(disp_inv))]).T
        retval, dst = cv.solve(coeff, z, flags=cv.DECOMP_QR)
        M = dst[0, 0]
        C = dst[1, 0]

    print("Saving parameters...")
    cv_file_write = cv.FileStorage(DESTINATION_PATH, cv.FILE_STORAGE_WRITE)
    cv_file_write.write('num_disparities', min(num_disparities/16, 16))
    cv_file_write.write('block_size', max(block_size_disp/2 - 5, 0))
    cv_file_write.write('pre_filter_type', pre_filter_type)
    cv_file_write.write('pre_filter_size', max(pre_filter_size/2 - 5, 0))
    cv_file_write.write('pre_filter_cap', pre_filter_cap - 1)
    cv_file_write.write('texture_threshold', texture_threshold)
    cv_file_write.write('uniqueness_ratio', uniqueness_ratio)
    cv_file_write.write('speckle_range', speckle_range)
    cv_file_write.write('speckle_window_size', speckle_window_size/2)
    cv_file_write.write('disparity_max_diff', disparity_max_diff)
    cv_file_write.write('min_disparity', min_disparity)
    cv_file_write.write('obstacle_area', obs_area * 1000)
    cv_file_write.write('contour_area', cont_area * 1000)
    cv_file_write.write('M', M)
    cv_file_write.release()
