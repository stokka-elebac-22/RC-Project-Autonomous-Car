'''Importing necessary libraries'''
import dataclasses
import os.path
import cv2 as cv
import numpy as np

@dataclasses.dataclass
class DisparityParameters:
    # pylint: disable=too-many-instance-attributes
    # it seem reasonable in this case
    '''Disparity Parameters'''
    def __init__(self, path):
        self.num_disparities = 0
        self.block_size = 0
        self.measurement = 100

        if os.path.exists(path):
            cv_file_read = cv.FileStorage(path, cv.FILE_STORAGE_READ)
            self.num_disparities = cv_file_read.getNode('num_disparities').real()
            self.block_size = cv_file_read.getNode('block_size').real()
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
        # stereoSGBM
        self.stereo = cv.StereoSGBM_create(
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

        disparity = self.stereo.compute(rect_left, rect_right)
        # NOTE: Code returns a 16bit signed single channel image (CV_16S),
        # containing a disparity map scaled by 16.
        # Hence it is essential to convert it to CV_32F and scale it down 16 times.

        # Converting to float32
        disparity = disparity.astype(np.float32)

        # Scaling down the disparity values and normalizing them
        disparity = (disparity/16.0)/self.parameters.num_disparities
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

    def obstacle_detection(self, disparity, min_dist, max_dist): # pylint: disable=R0914
        '''Detecting depth to obstacles in cm'''
        depth_map = self.parameters.measurement/disparity # for depth in cm
        param = 0.01

        mask = cv.inRange(depth_map, min_dist, max_dist)

        if np.sum(mask)/255.0 > param*mask.shape[0]*mask.shape[1]:
		    # Contour detection
            contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            cnts = sorted(contours, key=cv.contourArea, reverse=True)

            x_pos, y_pos, w_rect, h_rect = None, None, None, None
            cur_cnt = None
            current_average_value = np.average(cnts[0])

            for cnt in cnts: # go through every contours
		        # Check if detected contour is significantly large (to avoid multiple tiny regions)
                if cv.contourArea(cnt) > param*mask.shape[0]*mask.shape[1]:
                    if np.average(cnt) > current_average_value:
                        continue
                    x_pos, y_pos, w_rect, h_rect = cv.boundingRect(cnt)
                    cur_cnt = cnt
            if cur_cnt is None:
                return False, None, None, None
			# finding average depth of region represented by the largest contour
            mask2 = np.zeros_like(mask)
            cv.drawContours(mask2, cur_cnt, 0, (255), -1)
			# Calculating the average depth of the object closer than the safe distance
            depth_mean, _ = cv.meanStdDev(depth_map, mask=mask2)
            if depth_mean:
                return True, depth_mean, (x_pos, y_pos), (w_rect, h_rect)
        return False, None, None, None

    def get_data(self, disparity, min_dist, max_dist):
        '''Returns bool value, depth, position and size'''
        retval, depth, pos, size = self.obstacle_detection(
            disparity,
            min_dist,
            max_dist)

        return retval, depth, pos, size


if __name__ == '__main__':
    from camera import Camera
    # PARAMETER_PATH = 'computer_vision/stereoscopic_vision/data/stereo_parameters.xml'
    PARAMETER_PATH = 'computer_vision/stereoscopic_vision/data/stereo_parameters.xml'
    MAPS_PATH = 'computer_vision/stereoscopic_vision/data/stereo_rectify_maps_web_light.xml'
    MAX_DIST = 2000 # max distance to recognize objects (mm)
    MIN_DIST = 50 # min distance to recognize objects (mm)
    BLUR = 12
    M = 1 # base value, the real one is from the xml file (and is calculated in a previous test)
    Z = MAX_DIST # The depth, for used for calculating M
    DISPLAY = False

    # NOTE: if you also have a webcam (that you do not want to use),
    cam_left = Camera(camera_id=2, window_name='Left camera')
    cam_right = Camera(camera_id=1, window_name='Right camera')
    stereo_vision = StereoscopicVision(MAPS_PATH, PARAMETER_PATH)

    if DISPLAY:
        cv.namedWindow('disp', cv.WINDOW_NORMAL)
        cv.namedWindow('disparity', cv.WINDOW_NORMAL)

        def nothing(_):
            '''Empty function'''

        print('Creating trackbars...')
        # creating trackbars for testing
        cv.createTrackbar('num_disparities','disp',1,17, nothing)
        cv.createTrackbar('block_size','disp',3,20,nothing)

    if DISPLAY:
        print('Setting trackbar positions...')
        # Getting parameter information from previous tests, if there is one
        if os.path.exists(PARAMETER_PATH):
            file_read = cv.FileStorage(PARAMETER_PATH, cv.FILE_STORAGE_READ)
            cv.setTrackbarPos('num_disparities','disp',
                int(stereo_vision.parameters.num_disparities/16))
            cv.setTrackbarPos('block_size','disp',
                int((stereo_vision.parameters.block_size-5)/2))
            M = file_read.getNode('M').real()
            file_read.release()

    CURRENT_DEPTH = 500
    STEP_SIZE = 200 # Reduce the current depth by step size for every mouse press
    value_pairs = [] # used for calculating M (depth ratio)

    average = [0 for _ in range(10)]

    # Defining callback functions for mouse events
    # pylint: disable=W0613
    if DISPLAY:
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
                    CURRENT_DEPTH += STEP_SIZE


        cv.setMouseCallback('disparity', mouse_click)

    # DIRECTORY_LEFT_IMAGE = \
    #     'computer_vision/stereoscopic_vision/images/test_images/frame left.png'
    # DIRECTORY_RIGHT_IMAGE = \
    #     'computer_vision/stereoscopic_vision/images/test_images/frame right.png'

    # if not os.path.exists(DIRECTORY_LEFT_IMAGE):
    #     print(f'{DIRECTORY_LEFT_IMAGE} does not exists')
    #     raise FileExistsError
    # if not os.path.exists(DIRECTORY_RIGHT_IMAGE):
    #     print(f'{DIRECTORY_RIGHT_IMAGE} does not exists')
    #     raise FileExistsError

    print('Running...')
    while True:
        ret_left, frame_left = cam_left.read()
        ret_right, frame_right = cam_right.read()
        # ret_left, ret_right = True, True
        # frame_left = cv.imread(DIRECTORY_LEFT_IMAGE)
        # frame_right = cv.imread(DIRECTORY_RIGHT_IMAGE)
        frame_left = cv.blur(frame_left,(BLUR, BLUR))
        frame_right = cv.blur(frame_right,(BLUR, BLUR))

        if ret_left and ret_right:
            # NOTE: it might help to blur the image to reduce noise
            # Displaying the disparity
            # Updating the parameters based on the trackbar positions
            if DISPLAY:
                gtp_num_disparities = cv.getTrackbarPos('num_disparities', 'disp')
                gtp_block_size = cv.getTrackbarPos('block_size','disp')

                stereo_vision.parameters.num_disparities = max(gtp_num_disparities*16, 16)
                stereo_vision.parameters.block_size = gtp_block_size*2 + 5

                # # Setting the updated parameters before computing disparity map
                stereo_vision.stereo.setNumDisparities(stereo_vision.parameters.num_disparities)
                stereo_vision.stereo.setBlockSize(stereo_vision.parameters.block_size)

            current_disparity = stereo_vision.get_disparity(frame_left, frame_right)
            ret_val, depth_val, pos_val, size_val = stereo_vision.get_data(
                current_disparity, MIN_DIST, MAX_DIST)

            if ret_val and depth_val[0][0] is not None:
                average.pop()
                average.append(depth_val[0][0])
                if DISPLAY:
                    cv.putText(frame_left, f'{int(np.sum(average)/len(average))} cm',
                        [pos_val[0] + 5, pos_val[1] + 40], 1, 2, (40, 200, 40), 2, 2)
                    cv.rectangle(current_disparity,
                        pos_val,
                        (pos_val[0] + size_val[0], pos_val[1] + size_val[1]),
                        color=(255, 200, 40))
                else:
                    print(int(np.sum(average)/len(average)))

            if DISPLAY:
                cv.imshow('frame left', frame_left)
                cv.imshow('frame right', frame_right)
                cv.imshow('disparity', current_disparity)

            if CURRENT_DEPTH < MIN_DIST:
                break

            if cv.waitKey(1) & 0xFF == ord('q'):
                print('Quitting...')
                break

    if DISPLAY:
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
    # if CURRENT_DEPTH < MIN_DIST: # only write if testing
    #     cv_file_write.write('M', M)
    # cv_file_write.release()
