'''Import libraries'''
import warnings
from typing import Union, TypedDict
import sys
import os
import cv2
import numpy as np
try:
    from line_detector import LineDetector
except ImportError:
    try:
        from computer_vision.line_detection.line_detector import LineDetector
        from computer_vision.qr_code.qr_code import QRCode
    except ImportError:
        from line_detection.line_detector import LineDetector

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from qr_code.qr_code import QRCode

class ParkingSlotDetector(LineDetector):
    '''DOC: Detects parking slot'''
    # pylint: disable=R0913
    def __init__(self,
                 canny: list[int, int] = None,
                 blur: int = 3,
                 hough: list[int, int] = None,
                 iterations: list[int, int] = None,
                 filter_atol: list[int, int] = None,
                 cluster_atol: int = 5):
        '''Initialize the Line Detector'''
        LineDetector.__init__(self, canny, blur, hough, iterations)

        if filter_atol is None:
            filter_atol = [20, 20]
        self.cluster_atol = cluster_atol
        self.filter_atol = filter_atol
        self.qr_slope = 0
        self.qr_intercept = 0

    def get_region_of_interest(self, image: np.ndarray) -> np.ndarray:
        '''
        Calculate the region of interest,
        '''
        black_image = np.zeros_like(image)
        mask_points = np.array([[(0, int(self.qr_intercept)),
                                 (image.shape[1], int(
                                     self.qr_slope*image.shape[1]+self.qr_intercept)),
                                 (image.shape[1], image.shape[0]), (0, image.shape[0])]])
        mask = cv2.fillPoly(black_image, mask_points, (255, 255, 255))
        roi = cv2.bitwise_and(image, mask)
        return roi

    def get_group_lines(self, lines: np.ndarray) -> list[list[np.ndarray], list[np.ndarray]]: # pylint: disable=R0914
        '''Group lines that are close to each other'''
        group_lines = []
        group_coords = []
        for line in lines:
            x_1, y_1, x_2, y_2 = line.reshape(4)
            with warnings.catch_warnings():
                warnings.filterwarnings('error')
                try:
                    parameters = np.polyfit((x_1, x_2), (y_1, y_2), 1)
                    slope = parameters[0]
                    intercept = parameters[1]

                    if len(group_lines) == 0:
                        group_lines.append([(slope, intercept)])
                        group_coords.append(
                            [np.array([x_1, y_1, x_2, y_2])])
                    else:
                        not_stopped = True
                        # Check which cluster the line fits into
                        for i, group in enumerate(group_lines):
                            avg_line = np.average(group, axis=0)
                            if np.isclose(avg_line, (slope, intercept),
                                          atol=self.cluster_atol, rtol=1e-9).all():
                                group.append((slope, intercept))
                                group_coords[i].append(
                                    np.array([x_1, y_1, x_2, y_2]))
                                not_stopped = False
                                break
                        # If not, a new cluster
                        if not_stopped:
                            group_lines.append([(slope, intercept)])
                            group_coords.append(
                                [np.array([x_1, y_1, x_2, y_2])])
                except np.RankWarning:
                    pass
                except RuntimeWarning:
                    pass
        return group_lines, group_coords

    def get_clustered_lines(self, lines: list[np.ndarray]) -> list[np.ndarray, np.ndarray]:
        '''Retrieve the clustered lines'''
        group_lines, group_coords = self.get_group_lines(lines)

        # calculate average line and coordinates of the clustered lines
        clustered_coords = []
        clustered_lines = []
        for i, cluster in enumerate(group_lines):
            line = np.average(cluster, axis=0)
            clustered_lines.append(line)
            min_x, max_x = self.get_min_max_x(group_coords[i])
            coordinates = self.get_line_coordinates_from_parameters(
                min_x, max_x, line)
            clustered_coords.append(coordinates)
        return clustered_lines, clustered_coords


    def filter_lines(self,
                     lines: list[np.ndarray],
                     coords: list[np.ndarray]) -> None:
        'Filter lines that are close to the qr-code'
        temp_coords = []
        temp_lines = []
        for i, line in enumerate(lines):
            if not (np.isclose(self.qr_slope, line[0], atol=self.filter_atol[0], rtol=1e-9) and
                    np.isclose(self.qr_intercept, line[1], atol=self.filter_atol[1], rtol=1e-9)):
                temp_lines.append(line)
                temp_coords.append(coords[i])
        return temp_lines, temp_coords

    def get_min_max_x(self, coordinates: list[np.ndarray]) -> list[int, int]:
        '''Get the minimum and maximum x values from a set of coordinates'''
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
        '''Get the closest line to the QR code'''
        lines = []
        left_diff = None
        left_index = 0
        right_index = 0
        right_diff = None

        for i, coords in enumerate(line_coords):

            min_value = min(coords[1], coords[3])
            min_index = np.where(coords == min_value)[0][0]
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
                        left_diff = point[0] - points[3][0]
            elif point[0] - points[2][0] >= 0:
                if right_diff is None:
                    right_index = i
                    right_diff = point[0] - points[2][0]
                else:
                    if point[0] - points[2][0] < right_diff:
                        right_index = i
                        right_diff = point[0] - points[2][0]
        if len(line_coords) > left_index and len(line_coords) > right_index:
            lines = [line_coords[left_index], line_coords[right_index]]
            return lines
        return None

    QrData = TypedDict('QrData', {
        'ret': bool,
        'points': np.ndarray
    })

    def get_parking_lines(self, image: np.ndarray) -> list[list[np.ndarray], list[np.ndarray]]:
        '''Get all parking lines in an image'''
        lines = self.get_lines(image)
        if lines is None:
            return None

        clustered_lines, clustered_coords = self.get_clustered_lines(lines)
        return clustered_lines, clustered_coords

    def get_parking_slot(self,
                             image: np.ndarray,
                             qr_data: QrData
                             ) -> Union[list[np.ndarray], None]:
        '''Detect the parking lines in the image'''
        if qr_data['ret']:
            self.qr_slope, self.qr_intercept = np.polyfit(
                (qr_data['points'][0][2][0],
                 qr_data['points'][0][3][0]),
                (qr_data['points'][0][2][1],
                 qr_data['points'][0][3][1]), 1)
            line_and_coords = self.get_parking_lines(image)
            if line_and_coords is not None:
                clustered_lines, clustered_coords = self.get_parking_lines(image)
                # filter away lines that are close to the QR-code
                _, avg_lines_coords = self.filter_lines(
                    clustered_lines, clustered_coords)

                # find the two closesqt lines to the QR-code
                lines = self.get_closest_line(
                    avg_lines_coords, qr_data['points'][0])
                return lines
        return None

    def get_line_coordinates_from_parameters(self,
                                             min_x: int,
                                             max_x: int,
                                             line_parameters: list[float, float]) -> np.ndarray:
        '''Get line coordinates from line parameters'''
        slope = line_parameters[0]
        intercept = line_parameters[1]
        y_1 = int(slope*min_x + intercept)
        y_2 = int(slope*max_x + intercept)
        x_1 = min_x
        x_2 = max_x
        return np.array([x_1, y_1, x_2, y_2])

    def get_closing_line_of_two_lines(self, lines):
        '''Get the line that closes the two parking lines'''
        line_coords = []
        if len(lines) == 2:
            for line in lines:
                max_value = min(line[1], line[3])
                min_index = np.where(line == max_value)[0][0]
                if min_index == 1:
                    line_coords.append(line[0])
                    line_coords.append(line[1])
                else:
                    line_coords.append(line[2])
                    line_coords.append(line[3])
        return np.array(line_coords)


if __name__ == '__main__':
    # ORIGINAL: hough=[200,5]
    parking_slot_detector = ParkingSlotDetector(
        hough=[200, 5], iterations=[5, 2])
    img = cv2.imread('computer_vision/line_detection/assets/parking/10.png')
    qr_size = {
        'px': 76,
        'mm': 52,
        'distance': 500
    }
    qr_code = QRCode(size=qr_size)
    data = qr_code.get_data(img)
    qr_code_data = {
        'ret': data['ret'],
        'points': data['points']
    }
    qr_code_measurements = {
        'distances': data['distances'],
        'angles': data['angles'],
        'info': data['info']}
    qr_code.display(img, qr_code_measurements, verbose=2)

    parking_lines = parking_slot_detector.get_parking_slot(img, qr_code_data)
    parking_lines.append(
        parking_slot_detector.get_closing_line_of_two_lines(parking_lines))
    parking_slot_detector.show_lines(img, parking_lines)
    # test_lines, test_coords = parking_slot_detector.get_parking_lines(img)
    # parking_slot_detector.show_lines(img, test_coords)
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()