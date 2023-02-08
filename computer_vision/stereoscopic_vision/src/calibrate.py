"""
source: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_calib3d/
py_calibration/py_calibration.html#calibration

https://learnopencv.com/making-a-low-cost-stereo-camera-using-opencv/

the code is highly inspired from the sources, but modified to fit our use case
"""
import glob
import numpy as np
import cv2 as cv

class Calibrate:
    """Calibrating two cameras"""
    def __init__(self, criteria, board_dim=(8, 6), dir_left="", dir_right=""):
        self.board_dim = board_dim
        self.dir_left = dir_left
        self.dir_right = dir_right
        self.criteria = criteria

        # prepare object points
        self.obj_pnt = np.zeros((self.board_dim[0]*self.board_dim[1], 3), np.float32)
        self.obj_pnt[:, :2] = np.mgrid[0:self.board_dim[0], 0:self.board_dim[1]].T.reshape(-1, 2)

    def calculate_object_and_image_points(self):
        """Calculate object points and image points for valid images"""
        # arrays to store object poitns and image points from all the images
        object_points = []
        image_points_left = []
        image_points_right = []

        images_left = glob.glob(self.dir_left)
        images_right= glob.glob(self.dir_right)

        images_returned_left = []
        images_returned_right = []

        for left, right in zip(images_left, images_right):
            image_left = cv.imread(left)
            image_right = cv.imread(right)
            gray_left = cv.cvtColor(image_left, cv.COLOR_BGR2GRAY)
            gray_right = cv.cvtColor(image_right, cv.COLOR_BGR2GRAY)

            # find the chess board corners
            ret_left, corners_left = cv.findChessboardCorners(gray_left, self.board_dim, None)
            ret_right, corners_right = cv.findChessboardCorners(gray_right, self.board_dim, None)

            # if found, add object point, image point (after refining them)
            if ret_left and ret_right:
                object_points.append(self.obj_pnt)
                images_returned_left.append(left)
                images_returned_right.append(right)

                corners_left = cv.cornerSubPix(
                    gray_left, corners_left, (11, 11), (-1, -1), self.criteria)
                image_points_left.append(corners_left)
                corners_right = cv.cornerSubPix(
                    gray_right, corners_right, (11, 11), (-1, -1), self.criteria)
                image_points_right.append(corners_right)
                # draw and display the corners
                cv.drawChessboardCorners(image_left, self.board_dim, corners_left, ret_left)
                cv.drawChessboardCorners(image_right, self.board_dim, corners_right, ret_right)
                cv.imshow("left", image_left)
                cv.imshow("right", image_right)
                cv.waitKey(0)
        print(f"""Could find chessboard corners in {len(object_points)}
        out of {len(images_left)} images""")

        cv.destroyAllWindows()

        return object_points, image_points_left, image_points_right, \
            images_returned_left, images_returned_right

    def get_optimal_new_camera_matrix(self, img, mtx, dist):
        """return optimal camera matrix with cv.getOptimalNewCameraMatrix"""
        height, width = img.shape[:2]
        new_camera_matrix, roi = \
            cv.getOptimalNewCameraMatrix(mtx, dist, (width, height), 1, (width, height))
        return new_camera_matrix, roi

    def undistort(self, img, mtx, dist, new_camera_matrix, roi):
        """Undistort the image"""
        height, width = img.shape[:2]
        # undistort
        mapx, mapy = \
            cv.initUndistortRectifyMap(mtx, dist, None, new_camera_matrix, (width, height), 5)
        dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

        # crop image
        pos_x, pos_y, roi_width, roi_height = roi
        dst = dst[pos_y:pos_y+roi_height, pos_x:pos_x+roi_width]

        # cv.imwrite('Stereoscopic Vision\images\calibrate_results\calibrated.png', dst)

    def re_projection_error(self, object_points, image_points, rvecs, tvecs, mtx, dist):
        """
        # From the source 1:
        # Re-projection error gives a good estimation of just how exact is the found parameters.
        # This should be as close to 0 as possible.
        """

        mean_error = 0
        total_error = 0
        # for i in range(len(object_points)):
        for object_point, image_point, rvec, tvec in zip(object_points, image_points, rvecs, tvecs):
            image_point, _ = cv.projectPoints(object_point, rvec, tvec, mtx, dist)
            error = cv.norm(image_point, image_point, cv.NORM_L2)/len(image_point)
            total_error += error

        print(f"total error: {mean_error/len(object_points)}")

if __name__ == '__main__':
    CHECKERBOARD_DIMENSION = (8, 6)
    CRITERIA = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    DIRECTORY_LEFT = "computer_vision/stereoscopic_vision/images/calibrate_large/left/*.jpg"
    DIRECTORY_RIGHT = "computer_vision/stereoscopic_vision/images/calibrate_large/right/*.jpg"
    DESTINATION_PATH = "computer_vision/stereoscopic_vision/data/stereo_rectify_maps_large.xml"

    # Calibrate left camera
    calibrate = Calibrate(CRITERIA, CHECKERBOARD_DIMENSION, DIRECTORY_LEFT, DIRECTORY_RIGHT)
    obj_pnts, img_pnts_l, img_pnts_r, img_l, img_r= calibrate.calculate_object_and_image_points()

    image_l = cv.imread(img_l[0])
    gray_l = cv.cvtColor(image_l, cv.COLOR_BGR2GRAY)
    image_r = cv.imread(img_r[0])
    gray_r = cv.cvtColor(image_r, cv.COLOR_BGR2GRAY)

    ret_1, mtx_l, dist_l, rvecs_l, tvecs_l = \
        cv.calibrateCamera(obj_pnts, img_pnts_l, gray_l.shape[::-1], None, None)
    ret_r, mtx_r, dist_r, rvecs_r, tvecs_r = \
        cv.calibrateCamera(obj_pnts, img_pnts_r, gray_r.shape[::-1], None, None)

    new_camera_matrix_left, roi_left = \
        calibrate.get_optimal_new_camera_matrix(gray_l, mtx_l, dist_l)
    new_camera_matrix_right, roi_right = \
        calibrate.get_optimal_new_camera_matrix(gray_r, mtx_r, dist_r)
    # calibrate.undistort(img, mtx_left, left_dist, new_camera_matrix_left, roi_left)

    # Stereo Calibration
    FLAGS = 0
    FLAGS |= FLAGS
    retS, new_mtx_left, dist_left, new_mtx_right, dist_right, Rot, Trns, Emat, Fmat = \
        cv.stereoCalibrate(
        obj_pnts,
        img_pnts_l,
        img_pnts_r,
        new_camera_matrix_left,
        dist_l,
        new_camera_matrix_right,
        dist_r,
        gray_l.shape[::-1],
        CRITERIA,
        FLAGS)

    # Stereo Rectification
    RECTIFY_SCALE = 1
    rect_l, rect_r, proj_mat_l, proj_mat_r, Q, roi_l, roi_r = cv.stereoRectify(
        new_mtx_left,
        dist_left,
        new_mtx_right,
        dist_right,
        gray_l.shape[::-1],
        Rot,
        Trns,
        RECTIFY_SCALE,
        (0, 0))

    stereo_map_left = cv.initUndistortRectifyMap(
        new_mtx_left,
        dist_l,
        rect_l,
        proj_mat_l,
        gray_l.shape[::-1],
        cv.CV_16SC2)
    stereo_map_right = cv.initUndistortRectifyMap(
        new_mtx_right,
        dist_right,
        rect_r,
        proj_mat_r,
        gray_r.shape[::-1],
        cv.CV_16SC2)

    print("Saving parameters...")
    cv_file = cv.FileStorage(DESTINATION_PATH, cv.FILE_STORAGE_WRITE)
    cv_file.write("stereo_map_left_x", stereo_map_left[0])
    cv_file.write("stereo_map_left_y", stereo_map_left[1])
    cv_file.write("stereo_map_right_x", stereo_map_right[0])
    cv_file.write("stereo_map_right_y", stereo_map_right[1])
    cv_file.release()
