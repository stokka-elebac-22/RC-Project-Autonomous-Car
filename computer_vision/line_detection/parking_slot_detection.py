"""Import libraries"""
import warnings
from typing import Union
import sys
import os
import cv2
import numpy as np
#from main import LineDetector
from computer_vision.line_detection.main import LineDetector
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from qr_code.qr_code import QRCode

class ParkingSlotDetector(LineDetector):
    """
    DOC: Detects parking slot
    """

    def __init__(self,
                 canny: list[int, int] = None,
                 blur: int = 3,
                 hough: list[int, int] = None,
                 iterations: list[int, int] = None):
        '''Initialize the Line Detector'''
        LineDetector.__init__(self, canny, blur, hough, iterations)

    def __get_qr_code_info(self,
                           image: np.ndarray,
                           qr_size_px: int,
                           qr_size_mm: int,
                           qr_distance: int) -> list[QRCode, dict]:
        '''Use the QR-code module to get the info needed'''
        qr_code = QRCode(qr_size_px, qr_size_mm, qr_distance)
        return qr_code, qr_code.get_data(image)

    def cluster_lines(self, lines: np.ndarray, atol: int =5) -> list[np.ndarray, np.ndarray]:
        '''Cluster lines that are close to each other'''
        clustered_lines = []
        clustered_coords = []
        for line in lines:
            x_1, y_1, x_2, y_2 = line.reshape(4)
            with warnings.catch_warnings():
                warnings.filterwarnings('error')
                try:
                    parameters = np.polyfit((x_1, x_2), (y_1, y_2), 1)
                    slope = parameters[0]
                    intercept = parameters[1]

                    if len(clustered_lines) == 0:
                        clustered_lines.append([(slope, intercept)])
                        clustered_coords.append(
                            [np.array([x_1, y_1, x_2, y_2])])
                    else:
                        not_stopped = True
                        # Check which cluster the line fits into
                        for i, cluster in enumerate(clustered_lines):
                            cluster_line_avg = np.average(cluster, axis=0)
                            if np.isclose(cluster_line_avg, (slope, intercept),
                                          atol=atol, rtol=1e-9).all():
                                cluster.append((slope, intercept))
                                clustered_coords[i].append(
                                    np.array([x_1, y_1, x_2, y_2]))
                                not_stopped = False
                                break
                        # If not, a new cluster
                        if not_stopped:
                            clustered_lines.append([(slope, intercept)])
                            clustered_coords.append(
                                [np.array([x_1, y_1, x_2, y_2])])
                except np.RankWarning:
                    pass
        return clustered_lines, clustered_coords

    def filter_lines(self,
                     lines: list[np.ndarray],
                     coords: list[np.ndarray],
                     slope: float,
                     intercept: float) -> None:
        'Filter lines that are close to the qr-code'
        temp_coords = []
        temp_lines = []
        for i, line in enumerate(lines):
            if not (np.isclose(slope, line[0], atol=20, rtol=1e-9) and
                    np.isclose(intercept, line[1], atol=20, rtol=1e-9)):
                temp_lines.append(line)
                temp_coords.append(coords[i])
        return temp_lines, temp_coords

    def get_min_max_x(self, coordinates: list[np.ndarray]) -> list[int, int]:
        """Get the minimum and maximum x values from a set of coordinates"""
        max_values = np.argmax(coordinates, axis=0)
        max_x = np.max([coordinates[max_values[0]]
                        [0], coordinates[max_values[2]][2]])
        min_values = np.argmin(coordinates, axis=0)
        min_x = np.min([coordinates[min_values[0]]
                        [0], coordinates[min_values[2]][2]])
        return min_x, max_x

    def get_closest_line(self,
                         line_coords: list[np.ndarray],
                         points: np.ndarray,
                        ) -> list[np.ndarray]:
        """Get the closest line based on the Y value"""
        lines = []
        left_diff = None
        left_index = 0
        right_index = 0
        right_diff = None

        for i, coords in enumerate(line_coords):

            min_value = min(coords[1], coords[3])
            min_index=np.where(coords==min_value)[0][0]
            if min_index == 1:
                point = [coords[0], coords[1]]
            else:
                point = [coords[2], coords[3]]

            if point[0] - points[3][0] <= 0:
                if left_diff is None:
                    left_index = i
                    left_diff = point[0] - points[3][0]
                else:
                    if point[0] - points[3][0] > left_diff:
                        left_index = i
                        left_diff = point[0]- points[3][0]
            elif point[0] - points[2][0] >= 0:
                if right_diff is None:
                    right_index = i
                    right_diff = point[0] - points[2][0]
                else:
                    if point[0] - points[2][0] < right_diff:
                        right_index = i
                        right_diff = point[0]- points[2][0]

        lines=[line_coords[left_index], line_coords[right_index]]
        return lines

    def detect_parking_lines(self,
                             image: np.ndarray,
                             qr_size_px: int,
                             qr_size_mm: int,
                             qr_distance: int) -> Union[list[np.ndarray], None]:
        "Detect the parking lines in the image"
        qrc,  data = self.__get_qr_code_info(
            image, qr_size_px, qr_size_mm, qr_distance)
        if data['ret']:
            # display QR-code on image
            qr_code_measurements = {
                'distances': data['distances'],
                'angles': data['angles'],
                'info': data['info']}

            qr_slope, qr_intercept = np.polyfit(
                (data['points'][0][2][0],
                 data['points'][0][3][0]),
                (data['points'][0][2][1],
                 data['points'][0][3][1]), 1)

            black_image = np.zeros_like(image)
            mask_points = np.array([[(0,int(qr_intercept)),
            (image.shape[1], int(qr_slope*image.shape[1]+qr_intercept)),
            (image.shape[1], image.shape[0]), (0, image.shape[0])]])
            mask = cv2.fillPoly(black_image, mask_points, (255, 255, 255))
            roi = cv2.bitwise_and(image, mask)
            qrc.display(image, qr_code_measurements, verbose=2)
            lines = self.get_lines(roi)
            if lines is None:
                return None

            clustered_lines, clustered_coords = self.cluster_lines(lines)

            # calculate average line and coordinates of the clustered lines
            avg_lines_coords = []
            avg_lines = []
            for i, cluster in enumerate(clustered_lines):
                line = np.average(cluster, axis=0)
                avg_lines.append(line)
                min_x, max_x = self.get_min_max_x(clustered_coords[i])
                coordinates = self.get_line_coordinates_from_parameters(
                    min_x, max_x, line)
                avg_lines_coords.append(coordinates)
            # filter away lines that are close to the QR-code
            avg_lines, avg_lines_coords = self.filter_lines(avg_lines, avg_lines_coords,
                              qr_slope, qr_intercept)

            # find the two closesqt lines to the QR-code
            lines = self.get_closest_line(
                avg_lines_coords, data['points'][0])
            return lines
        return None

    def get_line_coordinates_from_parameters(self,
                                             min_x: int,
                                             max_x: int,
                                             line_parameters: list[float, float]) -> np.ndarray:
        """Get line coordinates from line parameters"""
        slope = line_parameters[0]
        intercept = line_parameters[1]
        y_1 = int(slope*min_x + intercept)
        y_2 = int(slope*max_x + intercept)
        x_1 = min_x
        x_2 = max_x
        return np.array([x_1, y_1, x_2, y_2])


if __name__ == "__main__":
    # ORIGINAL: hough=[200,5]
    parking_slot_detector = ParkingSlotDetector(
        hough=[200, 5], iterations=[5, 2])
    img = cv2.imread('computer_vision/line_detection/assets/parking/13.png')
    QR_SIZE_PX = 76
    QR_SIZE_MM = 52
    QR_DISTANCE = 500
    parking_lines = parking_slot_detector.detect_parking_lines(
        img, QR_SIZE_PX, QR_SIZE_MM, QR_DISTANCE)
    parking_slot_detector.show_lines(img, parking_lines)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
