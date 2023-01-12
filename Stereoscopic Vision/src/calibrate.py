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

class Calibrate:
    def __init__(self, criteria, checkerboard_dimension=(8, 6), directory=""):
        self.checkerboard_dimension = checkerboard_dimension
        self.directory = directory
        self.criteria = criteria

        # prepare object points
        self.object_point = np.zeros((self.checkerboard_dimension[0]*self.checkerboard_dimension[1], 3), np.float32)
        self.object_point[:, :2] = np.mgrid[0:self.checkerboard_dimension[0], 0:self.checkerboard_dimension[1]].T.reshape(-1, 2)

    def calculate_object_and_image_points(self):
        # arrays to store object poitns and image points from all the images
        object_points = []
        image_points = []

        images = glob.glob(self.directory)

        for name in images:
            img = cv.imread(name)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            # find the chess board corners
            ret, corners = cv.findChessboardCorners(gray, self.checkerboard_dimension, None)

            # if found, add object point, image point (after refining them)
            if ret:
                object_points.append(self.object_point)

                cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
                image_points.append(corners)

                # draw and display the corners
                cv.drawChessboardCorners(img, self.checkerboard_dimension, corners, ret)
                # cv.imshow(name, img)
                # cv.waitKey(0)
        print(f"Could find chessboard corners in {len(object_points)} out of {len(images)} images")

        cv.destroyAllWindows()

        return object_points, image_points

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
    directory = 'Stereoscopic Vision/images/calibrate_left/*.jpg'
    calibrate = Calibrate(CRITERIA, CHECKERBOARD_DIMENSION, directory)
    images = glob.glob(directory) # get all images
    img_left = cv.imread(images[0]) # just choosing the first one (assuming it did find the checkerboard on that one...)
    gray_left = cv.cvtColor(img_left, cv.COLOR_BGR2GRAY) # making the img gray
    object_points, image_points_left = calibrate.calculate_object_and_image_points()
    left_ret, left_mtx, left_dist, left_rvecs, left_tvecs = calibrate.calibration(gray_left, object_points, image_points_left)
    left_new_camera_matrix, left_roi = calibrate.get_optimal_new_camera_matrix(img_left, left_mtx, left_dist)
    # calibrate.undistort(img, left_mtx, left_dist, left_new_camera_matrix, left_roi)

    # Calibrate right camera
    directory = 'Stereoscopic Vision/images/calibrate_right/*.jpg'
    calibrate = Calibrate(CRITERIA, CHECKERBOARD_DIMENSION, directory)
    images = glob.glob(directory) # get all images
    img_right = cv.imread(images[0]) # just choosing the first one (assuming it did find the checkerboard on that one...)
    gray_right = cv.cvtColor(img_right, cv.COLOR_BGR2GRAY) # making the img gray
    object_points, image_points_right = calibrate.calculate_object_and_image_points()
    right_ret, right_mtx, right_dist, right_rvecs, right_tvecs = calibrate.calibration(img_right, object_points, image_points_right)
    right_new_camera_matrix, right_roi = calibrate.get_optimal_new_camera_matrix(img_right, right_mtx, right_dist)
    # calibrate.undistort(img, left_mtx, left_dist, left_new_camera_matrix, left_roi)

    # Stereo Calibration
    retS, new_mtx_left, dist_left, new_mtx_right, dist_right, Rot, Trns, Emat, Fmat = stereo_calibrate(object_points, image_points_left, image_points_right, left_new_camera_matrix, left_dist, right_new_camera_matrix, right_dist, gray, CRITERIA)
    # Stereo Rectification
    rect_left, rect_right, proj_mat_left, proj_mat_right, Q, roi_left, roi_right, = stereo_rectify(new_mtx_left, left_dist, new_mtx_right, right_dist, gray_left, Rot, Trns)
    left_stereo_map = cv.initUndistortRectifyMap(new_mtx_left, left_dist, rect_left, proj_mat_left, gray_left.shape[::-1], cv.CV_16SC2)
    right_stereo_map = cv.initUndistortRectifyMap(new_mtx_right, right_dist, rect_right, proj_mat_right, gray_right.shape[::-1], cv.CV_16SC2)

    print("Saving parameters...")
    cv_file = cv.FileStorage("params.xml", cv.FILE_STORAGE_WRITE)
    cv_file.write("left_stereo_map_x", left_stereo_map[0])
    cv_file.write("left_stereo_map_y", left_stereo_map[1])
    cv_file.write("right_stereo_map_x", right_stereo_map[0])
    cv_file.write("right_stereo_map_y", right_stereo_map[1])
    cv_file.release()

