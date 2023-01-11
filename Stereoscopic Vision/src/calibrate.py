"""
source: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_calib3d/py_calibration/py_calibration.html#calibration

the code is highly inspired from the source, but modified to fit our use case
"""

import numpy as np
import cv2 as cv
import glob

CHECKERBOARD_DIMENSION = (8, 6)
DIRECTORY = 'Stereoscopic Vision/images/calibrate/*.jpg'
CRITERIA = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

class Calibrate:
    def __init__(self, criteria, checkerboard_dimension=(8, 6), directory=""):
        self.checkerboard_dimension = checkerboard_dimension
        self.directory = directory
        self.criteria = criteria

        # prepare object points
        object_point = np.zeros((self.checkerboard_dimension[0]*self.checkerboard_dimension[1], 3), np.float32)
        object_point[:, :2] = np.mgrid[0:self.checkerboard_dimension[0], 0:self.checkerboard_dimension[1]].T.reshape(-1, 2)

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
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(self.object_points, image_points, img.shape[::-1], None, None)

    def get_optimal_new_camera_matrix(self, img, mtx, dist):
        img = cv.imread(img) # just read the first image of the collection
        h, w = img.shape[:2]
        new_camera_matrix, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        return new_camera_matrix, roi

    def undistort(self, img, mtx, dist, new_camera_matrix, roi): 
        # undistort
        mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, new_camera_matrix, (w, h), 5)
        dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

        # crop image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]

        cv.imwrite(f'Stereoscopic Vision\images\calibrate_results\calibrated.png', dst)

    def re_projection_error(self, object_points, image_points, rvecs, tvecs, mtx, dist):
        ##### RE-PROJECTION ERROR #####
        # From the source:
        # Re-projection error gives a good estimation of just how exact is the found parameters. 
        # This should be as close to 0 as possible.

        mean_error = 0
        total_error = 0
        for i in range(len(object_points)):
            image_point, _ = cv.projectPoints(object_points[i], rvecs[i], tvecs[i], mtx, dist)
            error = cv.norm(image_points[i], image_point, cv.NORM_L2)/len(image_point)
            total_error += error

        print(f"total error: {mean_error/len(object_points)}")