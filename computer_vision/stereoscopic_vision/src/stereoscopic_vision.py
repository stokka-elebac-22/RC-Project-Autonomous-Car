'''Importing necessary libraries'''
import dataclasses
import os.path
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

@dataclasses.dataclass
class DisparityParameters:
    # pylint: disable=too-many-instance-attributes
    # it seem reasonable in this case
    '''Disparity Parameters'''
    def __init__(self, path):
        self.num_disparities = 0
        self.block_size = 0
        self.pre_filter_type = 0
        self.pre_filter_size = 0
        self.pre_filter_cap = 0
        self.texture_threshold = 0
        self.uniqueness_ratio = 0
        self.speckle_range = 0
        self.speckle_window_size = 0
        self.disparity_max_diff = 0
        self.min_disparity = 0
        self.obstacle_area = 0
        self.contour_area = 0
        self.measurement = 40

        if os.path.exists(path):
            cv_file_read = cv.FileStorage(path, cv.FILE_STORAGE_READ)
            self.num_disparities = cv_file_read.getNode('num_disparities').real()
            self.block_size = cv_file_read.getNode('block_size').real()
            self.pre_filter_type = cv_file_read.getNode('pre_filter_type').real()
            self.pre_filter_size = cv_file_read.getNode('pre_filter_size').real()
            self.pre_filter_cap = cv_file_read.getNode('pre_filter_cap').real()
            self.texture_threshold = cv_file_read.getNode('texture_threshold').real()
            self.uniqueness_ratio = cv_file_read.getNode('uniqueness_ratio').real()
            self.speckle_range = cv_file_read.getNode('speckle_range').real()
            self.speckle_window_size = cv_file_read.getNode('speckle_window_size').real()
            self.disparity_max_diff = cv_file_read.getNode('disparity_max_diff').real()
            self.min_disparity = cv_file_read.getNode('min_disparity').real()
            self.obstacle_area = cv_file_read.getNode('obstacle_area').real()
            self.contour_area = cv_file_read.getNode('contour_area').real()
            self.measurement = cv_file_read.getNode('M').real()
            cv_file_read.release()
        else:
            print(f"Path: '{path}' does not exists")

class StereoscopicVision:
    '''
    DOC:
    '''
    def __init__(self, path='', param_path='', disparity_parameters = None) -> None:
        if disparity_parameters is None:
            self.parameters = DisparityParameters(param_path)
        else: self.parameters = disparity_parameters

        # The path is the path to the calibration paramters (xml file)
        self.stereo_map_left, self.stereo_map_right = self.read_stereo_map(path)
        self.stereo = cv.StereoBM_create(
            numDisparities=int(self.parameters.num_disparities),
            blockSize=int(self.parameters.block_size))


    def get_disparity(self, image_left, image_right):
        '''Calculates and return the disparity'''
        gray_left = cv.cvtColor(image_left, cv.COLOR_BGR2GRAY)
        gray_right = cv.cvtColor(image_right, cv.COLOR_BGR2GRAY)

        # Applying stereo image rectification on the left image
        rect_left = cv.remap(
            gray_left,
            self.stereo_map_left[0],
            self.stereo_map_left[1],
            cv.INTER_LINEAR,
            cv.BORDER_CONSTANT,
            0)
        # Applying stereo image rectification on the right image
        rect_right = cv.remap(
            gray_right,
            self.stereo_map_right[0],
            self.stereo_map_right[1],
            cv.INTER_LINEAR,
            cv.BORDER_CONSTANT,
            0)

        # disparity = self.stereo.compute(gray_left, gray_right)
        disparity = self.stereo.compute(rect_left, rect_right)
        # NOTE: Code returns a 16bit signed single channel image (CV_16S),
        # containing a disparity map scaled by 16.
        # Hence it is essential to convert it to CV_32F and scale it down 16 times.

        # disparity = cv.normalize(disparity, disparity, alpha=255, beta=0, norm_type=cv.NORM_MINMAX)

        # Converting to float32
        disparity = disparity.astype(np.float32)

        # Scaling down the disparity values and normalizing them
        disparity = (disparity/16.0 - self.parameters.min_disparity)/self.parameters.num_disparities
        return disparity

    def read_stereo_map(self, path):
        '''Reading from stereo map xml file'''
        cv_file = cv.FileStorage(path, cv.FILE_STORAGE_READ)
        stereo_map_left_x = cv_file.getNode('stereo_map_left_x').mat()
        stereo_map_left_y = cv_file.getNode('stereo_map_left_y').mat()
        stereo_map_right_x = cv_file.getNode('stereo_map_right_x').mat()
        stereo_map_right_y = cv_file.getNode('stereo_map_right_y').mat()
        cv_file.release()
        return (stereo_map_left_x, stereo_map_left_y), (stereo_map_right_x, stereo_map_right_y)

    def obstacle_detection(self, depth_map, area, min_dist, thresh_dist):
        '''Detecting depth to obstacles in cm'''
        # Mask to segment regions with depth less than threshold
        mask = cv.inRange(depth_map, min_dist, thresh_dist)

        # Check if a significantly large obstacle is present and filter out smalle noisy regions
        if np.sum(mask)/255.0 > area['obstacle']*mask.shape[0]*mask.shape[1]:
            # Contour detection
            contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            # sorted have O(n log n) complexity
            # cnts = sorted(contours, key=cv.contourArea, reverse=True)

            x_pos, y_pos, w_rect, h_rect = None, None, None, None
            depth_mean = [[None]]
            # Because of the huge size of cnts,
            # a binary search method will be used instead of linear
            for cnt in contours:
                if cv.contourArea(cnt) > area['contour']*mask.shape[0]*mask.shape[1]:
                    # finding average depth of the contour
                    mask2 = np.zeros_like(mask)
                    cv.drawContours(mask2, cnt, 0, (255), -1)

                    # Calculating the average depth of the object closer than the safe distance
                    depth_mean_new, _ = cv.meanStdDev(depth_map, mask=mask2)
                    if depth_mean[0][0] is None or depth_mean_new[0][0] < depth_mean[0][0]:
                        depth_mean = depth_mean_new
                        x_pos, y_pos, w_rect, h_rect = cv.boundingRect(cnt)
            if depth_mean is None:
                return False, None, None, None
            return True, depth_mean, (x_pos, y_pos), (w_rect, h_rect)
        return False, None, None, None

    def get_data(self, disparity, min_dist, max_dist, thresh_dist):
        '''Returns bool value, depth, position and size'''
        depth_map_dist = self.parameters.measurement/disparity # for depth in cm
        mask_tmp = cv.inRange(depth_map_dist, min_dist, max_dist)
        depth_map_dist = cv.bitwise_and(depth_map_dist, depth_map_dist, mask=mask_tmp)

        area = {
            'obstacle': self.parameters.obstacle_area,
            'contour': self.parameters.contour_area
        }
        retval, depth, pos, size = self.obstacle_detection(
            depth_map_dist,
            area,
            min_dist,
            thresh_dist)

        return retval, depth, pos, size


if __name__ == '__main__':
    from camera import Camera
    PARAMETER_PATH = 'computer_vision/stereoscopic_vision/data/stereo_parameters.xml'
    MAPS_PATH = 'computer_vision/stereoscopic_vision/data/stereo_rectify_maps_large.xml'
    MAX_DIST = 4000 # max distance to recognize objects (mm)
    MIN_DIST = 500 # min distance to recognize objects (mm)
    THRESH_DIST = MAX_DIST
    M = 40 # base value, the real one is from the xml file (and is calculated in a previous test)
    Z = MAX_DIST # The depth, for used for calculating M

    # NOTE: if you also have a webcam (that you do not want to use),
    # use id 0 and 2 (not always the case....)
    cam_left = Camera(camera_id=0, window_name='Left camera')
    cam_right = Camera(camera_id=1, window_name='Right camera')
    stereo_vision = StereoscopicVision(MAPS_PATH, PARAMETER_PATH)

    cv.namedWindow('disp', cv.WINDOW_NORMAL)
    cv.namedWindow('disparity', cv.WINDOW_NORMAL)
    # cv.resizeWindow('disp', 800,600)

    def nothing(_):
        '''Empty function'''

    print('Creating trackbars...')
    # creating trackbars for testing
    cv.createTrackbar('num_disparities','disp',1,17, nothing)
    cv.createTrackbar('block_size','disp',5,50,nothing)
    # cv.createTrackbar('pre_filter_type','disp',1,1,nothing)
    # cv.createTrackbar('pre_filter_size','disp',2,25,nothing)
    # cv.createTrackbar('pre_filter_cap','disp',5,58,nothing)
    # cv.createTrackbar('texture_threshold','disp',10,100,nothing)
    # cv.createTrackbar('uniqueness_ratio','disp',15,100,nothing)
    # cv.createTrackbar('speckle_range','disp',0,100,nothing)
    # cv.createTrackbar('speckle_window_size','disp',3,25,nothing)
    # cv.createTrackbar('disparity_max_diff','disp',5,25,nothing)
    # cv.createTrackbar('min_disparity','disp',5,25,nothing)
    # cv.createTrackbar('obstacle_area', 'disp', 1, 100, nothing)
    # cv.createTrackbar('contour_area', 'disp', 1, 100, nothing)

    print('Setting trackbar positions...')
    # Getting parameter information from previous tests, if there is one
    # if os.path.exists(PARAMETER_PATH):
    #     file_read = cv.FileStorage(PARAMETER_PATH, cv.FILE_STORAGE_READ)
    #     cv.setTrackbarPos('num_disparities','disp',
    #         int(stereo_vision.parameters.num_disparities/16))
    #     cv.setTrackbarPos('block_size','disp',
    #         int((stereo_vision.parameters.block_size-5)/2))
        # cv.setTrackbarPos('pre_filter_type','disp',
        #     int(stereo_vision.parameters.pre_filter_type))
        # cv.setTrackbarPos('pre_filter_size','disp',
        #     int((stereo_vision.parameters.pre_filter_size-5)/2))
        # cv.setTrackbarPos('pre_filter_cap','disp',
        #     int(stereo_vision.parameters.pre_filter_cap))
        # cv.setTrackbarPos('texture_threshold','disp',
        #     int(stereo_vision.parameters.texture_threshold))
        # cv.setTrackbarPos('uniqueness_ratio','disp',
        #     int(stereo_vision.parameters.uniqueness_ratio))
        # cv.setTrackbarPos('speckle_range','disp',
        #     int(stereo_vision.parameters.speckle_range))
        # cv.setTrackbarPos('speckle_window_size','disp',
        #     int(stereo_vision.parameters.speckle_window_size))
        # cv.setTrackbarPos('disparity_max_diff','disp',
        #     int(stereo_vision.parameters.disparity_max_diff))
        # cv.setTrackbarPos('min_disparity','disp',
        #     int(stereo_vision.parameters.min_disparity))
        # cv.setTrackbarPos('obstacle_area', 'disp',
        #     int(stereo_vision.parameters.obstacle_area * 1000))
        # cv.setTrackbarPos('contour_area', 'disp',
        #     int(stereo_vision.parameters.contour_area * 1000))
        # M = file_read.getNode('M').real()
        # file_read.release()

    CURRENT_DEPTH = MAX_DIST
    STEP_SIZE = 500 # Reduce the current depth by step size for every mouse press
    value_pairs = [] # used for calculating M (depth ratio)

    average = [0 for _ in range(10)]

    # Defining callback functions for mouse events
    # pylint: disable=W0613
    def mouse_click(event, x_pos, y_pos, flags, param):
        '''Recognize when the mouse is pressed'''
        # pylint: disable=W0603
        global CURRENT_DEPTH
        if event == cv.EVENT_LBUTTONDBLCLK:
            print('Pressing...')
            if current_disparity[y_pos,x_pos] > 0:
                value_pairs.append([CURRENT_DEPTH, current_disparity[y_pos, x_pos]])
                print(f'Distance: {CURRENT_DEPTH} cm  | \
                    Disparity: {current_disparity[y_pos, x_pos]}')
                CURRENT_DEPTH -= STEP_SIZE

    cv.setMouseCallback('disparity', mouse_click)

    # DIRECTORY_LEFT_IMAGE = \
    #     'tests/images/stereoscopic_vision/distance/logi_1080p/left/left_300.jpg'
    # DIRECTORY_RIGHT_IMAGE = \
    #     'tests/images/stereoscopic_vision/distance/logi_1080p/right/right_300.jpg'
    DIRECTORY_LEFT_IMAGE = \
        'computer_vision/stereoscopic_vision/images/depth_test/left_2.jpg'
    DIRECTORY_RIGHT_IMAGE = \
        'computer_vision/stereoscopic_vision/images/depth_test/right_2.jpg'

    if not os.path.exists(DIRECTORY_LEFT_IMAGE):
        print(f'{DIRECTORY_LEFT_IMAGE} does not exists')
        raise FileExistsError
    if not os.path.exists(DIRECTORY_RIGHT_IMAGE):
        print(f'{DIRECTORY_RIGHT_IMAGE} does not exists')
        raise FileExistsError

    print('Running...')
    while True:
        # ret_left, frame_left = cam_left.read()
        # ret_right, frame_right = cam_right.read()
        ret_left, ret_right = True, True
        frame_left = cv.imread(DIRECTORY_LEFT_IMAGE)
        frame_right = cv.imread(DIRECTORY_RIGHT_IMAGE)

        if ret_left and ret_right:
            # NOTE: it might help to blur the image to reduce noise
            # Displaying the disparity
            # Updating the parameters based on the trackbar positions
            gtp_num_disparities = cv.getTrackbarPos('num_disparities', 'disp')
            gtp_block_size = cv.getTrackbarPos('block_size','disp')
            # gtp_pre_filter_type = cv.getTrackbarPos('pre_filter_type','disp')
            # gtp_pre_filter_size = cv.getTrackbarPos('pre_filter_size','disp')
            # gtp_pre_filter_cap = cv.getTrackbarPos('pre_filter_cap','disp')
            # gtp_texture_threshold = cv.getTrackbarPos('texture_threshold','disp')
            # gtp_uniqueness_ratio = cv.getTrackbarPos('uniqueness_ratio','disp')
            # gtp_speckle_range = cv.getTrackbarPos('speckle_range','disp')
            # gtp_speckle_window_size = cv.getTrackbarPos('speckle_window_size','disp')
            # gtp_disparity_max_diff = cv.getTrackbarPos('disparity_max_diff','disp')
            # gtp_min_disparity = cv.getTrackbarPos('min_disparity','disp')
            # gtp_obstacle_area = cv.getTrackbarPos('obstacle_area', 'disp')
            # gtp_contour_area = cv.getTrackbarPos('contour_area', 'disp')

            stereo_vision.parameters.num_disparities = max(gtp_num_disparities*16, 16)
            stereo_vision.parameters.block_size = gtp_block_size*2 + 5
            # stereo_vision.parameters.pre_filter_type = gtp_pre_filter_type
            # stereo_vision.parameters.pre_filter_size = gtp_pre_filter_size*2 + 5
            # stereo_vision.parameters.pre_filter_cap = max(gtp_pre_filter_cap, 1)
            # stereo_vision.parameters.texture_threshold = gtp_texture_threshold
            # stereo_vision.parameters.uniqueness_ratio = gtp_uniqueness_ratio
            # stereo_vision.parameters.speckle_range = gtp_speckle_range
            # stereo_vision.parameters.speckle_window_size = gtp_speckle_window_size
            # stereo_vision.parameters.disparity_max_diff = gtp_disparity_max_diff
            # stereo_vision.parameters.min_disparity = gtp_min_disparity
            # stereo_vision.parameters.obstacle_area = gtp_obstacle_area / 1000
            # stereo_vision.parameters.contour_area = gtp_contour_area / 1000

            # Setting the updated parameters before computing disparity map
            stereo_vision.stereo.setNumDisparities(stereo_vision.parameters.num_disparities)
            stereo_vision.stereo.setBlockSize(stereo_vision.parameters.block_size)
            # stereo_vision.stereo.setPreFilterType(stereo_vision.parameters.pre_filter_type)
            # stereo_vision.stereo.setPreFilterSize(stereo_vision.parameters.pre_filter_size)
            # stereo_vision.stereo.setPreFilterCap(stereo_vision.parameters.pre_filter_cap)
            # stereo_vision.stereo.setTextureThreshold(stereo_vision.parameters.texture_threshold)
            # stereo_vision.stereo.setUniquenessRatio(stereo_vision.parameters.uniqueness_ratio)
            # stereo_vision.stereo.setSpeckleRange(stereo_vision.parameters.speckle_range)
            # stereo_vision.stereo.setSpeckleWindowSize(stereo_vision.parameters.speckle_window_size)
            # stereo_vision.stereo.setDisp12MaxDiff(stereo_vision.parameters.disparity_max_diff)
            # stereo_vision.stereo.setMinDisparity(stereo_vision.parameters.min_disparity)

            current_disparity = stereo_vision.get_disparity(frame_left, frame_right)
            ret_val, depth_val, pos_val, size_val = stereo_vision.get_data(
                current_disparity, MIN_DIST, MAX_DIST, THRESH_DIST)

            if ret_val and depth_val[0][0] is not None:
                average.pop()
                average.append(depth_val[0][0])
                cv.putText(frame_left, f'{int(sum(average)/len(average))} cm',
                    [pos_val[0] + 5, pos_val[1] + 40], 1, 2, (40, 200, 40), 2, 2)
                cv.rectangle(current_disparity,
                    pos_val,
                    (pos_val[0] + size_val[0], pos_val[1] + size_val[1]),
                    color=(40, 200, 40))

            cv.imshow('frame left', frame_left)
            cv.imshow('frame right', frame_right)
            cv.imshow('disparity', current_disparity)
            # plt.imshow(current_disparity)
            # plt.axis('off')
            # plt.show()

            if CURRENT_DEPTH < MIN_DIST:
                break

            if cv.waitKey(1) & 0xFF == ord('q'):
                print('Quitting...')
                break

    cv.destroyWindow('disp')
    cv.destroyWindow('disparity')

    # Calculating the disparity list / inverse, solving M and C
    # Value paris should be 2 dimensional
    if len(value_pairs) > 0:
        value_pairs = np.array(value_pairs)
        z = value_pairs[:, 0]
        disp = value_pairs[:,1]
        disp_inv = 1/disp

        # Solving for M using least square fitting with QR decomposition method
        coeff = np.vstack([disp_inv, np.ones(len(disp_inv))]).T
        ret, dst = cv.solve(coeff, z, flags=cv.DECOMP_QR)
        M = dst[0, 0]
        C = dst[1, 0]
        print('Value of M: ', M)

    # print('Saving parameters...')
    # cv_file_write = cv.FileStorage(PARAMETER_PATH, cv.FILE_STORAGE_WRITE)
    # cv_file_write.write('num_disparities', stereo_vision.parameters.num_disparities)
    # cv_file_write.write('block_size', stereo_vision.parameters.block_size)
    # cv_file_write.write('pre_filter_type', stereo_vision.parameters.pre_filter_type)
    # cv_file_write.write('pre_filter_size', stereo_vision.parameters.pre_filter_size)
    # cv_file_write.write('pre_filter_cap', stereo_vision.parameters.pre_filter_cap)
    # cv_file_write.write('texture_threshold', stereo_vision.parameters.texture_threshold)
    # cv_file_write.write('uniqueness_ratio', stereo_vision.parameters.uniqueness_ratio)
    # cv_file_write.write('speckle_range', stereo_vision.parameters.speckle_range)
    # cv_file_write.write('speckle_window_size', stereo_vision.parameters.speckle_window_size)
    # cv_file_write.write('disparity_max_diff', stereo_vision.parameters.disparity_max_diff)
    # cv_file_write.write('min_disparity', stereo_vision.parameters.min_disparity)
    # cv_file_write.write('obstacle_area', stereo_vision.parameters.obstacle_area)
    # cv_file_write.write('contour_area', stereo_vision.parameters.contour_area)
    # if CURRENT_DEPTH < MIN_DIST: # only write if testing
    #     cv_file_write.write('M', M)
    # cv_file_write.release()
