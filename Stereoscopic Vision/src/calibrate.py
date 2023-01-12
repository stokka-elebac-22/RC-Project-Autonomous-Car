"""
source: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_calib3d/py_calibration/py_calibration.html#calibration
https://learnopencv.com/making-a-low-cost-stereo-camera-using-opencv/

the code is highly inspired from the sources, but modified to fit our use case
"""

import numpy as np
import cv2 as cv
import glob

CHECKERBOARD_DIMENSION = (8, 6)
CRITERIA = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
DIRECTORY_LEFT = "Stereoscopic Vision/images/calibrate_left/*.jpg"
DIRECTORY_RIGHT = "Stereoscopic Vision/images/calibrate_right/*.jpg"
DESTINATION_PATH = "Stereoscopic Vision/data/stereo_rectify_maps.xml"

class Calibrate:
    def __init__(self, criteria, checkerboard_dimension=(8, 6), directory_left="", directory_right=""):
        """
        This code is for calibrating two cameras at the same time
        """
        self.checkerboard_dimension = checkerboard_dimension
        self.directory_left = directory_left
        self.directory_right = directory_right
        self.criteria = criteria

        # prepare object points
        self.object_point = np.zeros((self.checkerboard_dimension[0]*self.checkerboard_dimension[1], 3), np.float32)
        self.object_point[:, :2] = np.mgrid[0:self.checkerboard_dimension[0], 0:self.checkerboard_dimension[1]].T.reshape(-1, 2)

    def calculate_object_and_image_points(self):
        # arrays to store object poitns and image points from all the images
        object_points = []
        image_points_left = []
        image_points_right = []

        images_left = glob.glob(self.directory_left)
        images_right= glob.glob(self.directory_right)

        images_returned_left = []
        images_returned_right = []

        for left, right in zip(images_left, images_right):
            image_left = cv.imread(left)
            image_right = cv.imread(right)
            gray_left = cv.cvtColor(image_left, cv.COLOR_BGR2GRAY)
            gray_right = cv.cvtColor(image_right, cv.COLOR_BGR2GRAY)

            # find the chess board corners
            ret_left, corners_left = cv.findChessboardCorners(gray_left, self.checkerboard_dimension, None)
            ret_right, corners_right = cv.findChessboardCorners(gray_right, self.checkerboard_dimension, None)

            # if found, add object point, image point (after refining them)
            if ret_left and ret_right:
                object_points.append(self.object_point)
                images_returned_left.append(left)
                images_returned_right.append(right)

                cv.cornerSubPix(gray_left, corners_left, (11, 11), (-1, -1), self.criteria)
                image_points_left.append(corners_left)
                cv.cornerSubPix(gray_right, corners_right, (11, 11), (-1, -1), self.criteria)
                image_points_right.append(corners_right)
                # draw and display the corners
                cv.drawChessboardCorners(image_left, self.checkerboard_dimension, corners_left, ret_left)
                cv.drawChessboardCorners(image_right, self.checkerboard_dimension, corners_right, ret_right)
                # cv.imshow("left", image_left)
                # cv.imshow("right", image_right)
                # cv.waitKey(0)
        print(f"Could find chessboard corners in {len(object_points)} out of {len(images_left)} images")

        cv.destroyAllWindows()

        return object_points, image_points_left, image_points_right, images_returned_left, images_returned_right

    def calibration(self, img, object_points, image_points):
        # calibrateCarmera returns the camera matrix, distortion coefficients, rotation and translation vectors
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(object_points, image_points, img.shape[::-1], None, None)
        return ret, mtx, dist, rvecs, tvecs

    def get_optimal_new_camera_matrix(self, img, mtx, dist):
        h, w = img.shape[:2]
        new_camera_matrix, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        return new_camera_matrix, roi

    def undistort(self, img, mtx, dist, new_camera_matrix, roi):
        h, w = img.shape[:2]
        # undistort
        mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, new_camera_matrix, (w, h), 5)
        dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

        # crop image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]

        cv.imwrite(f'Stereoscopic Vision\images\calibrate_results\calibrated.png', dst)

    def re_projection_error(self, object_points, image_points, rvecs, tvecs, mtx, dist):
        ##### RE-PROJECTION ERROR #####
        # From the source 1:
        # Re-projection error gives a good estimation of just how exact is the found parameters.
        # This should be as close to 0 as possible.

        mean_error = 0
        total_error = 0
        for i in range(len(object_points)):
            image_point, _ = cv.projectPoints(object_points[i], rvecs[i], tvecs[i], mtx, dist)
            error = cv.norm(image_points[i], image_point, cv.NORM_L2)/len(image_point)
            total_error += error

        print(f"total error: {mean_error/len(object_points)}")

def stereo_calibrate(object_points, img_points_left, img_points_right, new_mtx_left, dist_left, new_mtx_right, dist_right, img_left_gray, criteria_stereo, flags=cv.CALIB_FIX_INTRINSIC):
    """flag is set to fix the intrincisc camera matrices so that only Rot, Trns, Emat and Fmat are calculated"""
    flags = 0
    flags |= flags
    retS, new_mtx_left, dist_left, new_mtx_right, dist_right, Rot, Trns, Emat, Fmat = cv.stereoCalibrate(
        object_points,
        img_points_left,
        img_points_right,
        new_mtx_left,
        dist_left,
        new_mtx_right,
        dist_right,
        img_left_gray.shape[::-1],
        criteria_stereo,
        flags)
    return retS, new_mtx_left, dist_left, new_mtx_right, dist_right, Rot, Trns, Emat, Fmat

def stereo_rectify(new_mtx_left, dist_left, new_mtx_right, dist_right, img_left_gray, Rot, Trns, rectify_scale=1):
    rect_left, rect_right, proj_mat_left, proj_mat_r, Q, roi_left, roi_right = cv.stereoRectify(
        new_mtx_left,
        dist_left,
        new_mtx_right,
        dist_right,
        img_left_gray.shape[::-1],
        Rot,
        Trns,
        rectify_scale,
        (0, 0))
    return rect_left, rect_right, proj_mat_left, proj_mat_r, Q, roi_left, roi_right



if "__main__" == __name__:

    # Calibrate left camera
    calibrate = Calibrate(CRITERIA, CHECKERBOARD_DIMENSION, DIRECTORY_LEFT, DIRECTORY_RIGHT)
    object_points, image_points_left, image_points_right, images_left, images_right = calibrate.calculate_object_and_image_points()

    image_left = cv.imread(images_left[0])
    gray_left = cv.cvtColor(image_left, cv.COLOR_BGR2GRAY)
    image_right = cv.imread(images_left[0])
    gray_right = cv.cvtColor(image_left, cv.COLOR_BGR2GRAY)

    ret_left, mtx_left, left_dist, rvecs_left, tvecs_left = calibrate.calibration(gray_left, object_points, image_points_left)
    ret_right, mtx_right, dist_right, rvecs_right, tvecs_right = calibrate.calibration(gray_right, object_points, image_points_right)

    new_camera_matrix_left, roi_left = calibrate.get_optimal_new_camera_matrix(gray_left, mtx_left, left_dist)
    new_camera_matrix_right, roi_right = calibrate.get_optimal_new_camera_matrix(gray_right, mtx_right, dist_right)
    # calibrate.undistort(img, mtx_left, left_dist, new_camera_matrix_left, roi_left)

    # Stereo Calibration
    retS, new_mtx_left, dist_left, new_mtx_right, dist_right, Rot, Trns, Emat, Fmat = stereo_calibrate(
        object_points,
        image_points_left,
        image_points_right,
        new_camera_matrix_left,
        left_dist,
        new_camera_matrix_right,
        dist_right,
        gray_left,
        CRITERIA)
    # Stereo Rectification
    rect_left, rect_right, proj_mat_left, proj_mat_right, Q, roi_left, roi_right, = stereo_rectify(new_mtx_left, left_dist, new_mtx_right, dist_right, gray_left, Rot, Trns)
    stereo_map_left = cv.initUndistortRectifyMap(new_mtx_left, left_dist, rect_left, proj_mat_left, gray_left.shape[::-1], cv.CV_16SC2)
    stereo_map_right = cv.initUndistortRectifyMap(new_mtx_right, dist_right, rect_right, proj_mat_right, gray_right.shape[::-1], cv.CV_16SC2)

    print("Saving parameters...")
    cv_file = cv.FileStorage(DESTINATION_PATH, cv.FILE_STORAGE_WRITE)
    cv_file.write("stereo_map_left_x", stereo_map_left[0])
    cv_file.write("stereo_map_left_y", stereo_map_left[1])
    cv_file.write("stereo_map_right_x", stereo_map_right[0])
    cv_file.write("stereo_map_right_y", stereo_map_right[1])
    cv_file.release()

