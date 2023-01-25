"""Import libraries"""
import warnings
import sys
import os
import cv2
import numpy as np
#from main import LineDetector
from main import LineDetector
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from qr_code.qr_code import QRCode

class ParkingSlotDetector(LineDetector):
    """
    DOC: Detects parking slot
    """
    def __init__(self, canny=None, blur=3, hough=None, iterations=None):
        '''Initialize the Line Detector'''
        LineDetector.__init__(self, canny, blur, hough, iterations)

    def __get_qr_code_info(self, image, qr_size_px, qr_size_mm, qr_distance):
        '''Use the QR-code module to get the info needed'''
        qr_code = QRCode(qr_size_px, qr_size_mm, qr_distance)
        return qr_code, qr_code.get_data(image)

    def cluster_lines(self, lines, atol=10):
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

    def filter_lines(self, lines, coords, slope, intercept):
        """Filter lines that are not needed"""
        for i, line in enumerate(lines):
            # intercept atol = 20 ok for picture 7 and 8 but not for picture 4 need it for 150
            if (np.isclose(slope, line[0], atol=20, rtol=1e-9) and
            np.isclose(intercept, line[1], atol=20, rtol=1e-9)):
                lines.pop(i)
                coords.pop(i)

    def get_min_max_x(self, coordinates):
        """Get the minimum and maximum x values from a set of coordinates"""
        max_values = np.argmax(coordinates, axis=0)
        max_x = np.max([coordinates[max_values[0]]
                        [0], coordinates[max_values[2]][2]])
        min_values = np.argmin(coordinates, axis=0)
        min_x = np.min([coordinates[min_values[0]]
                        [0], coordinates[min_values[2]][2]])
        return min_x, max_x

    def get_closest_line(self, line_coords, points, amount, angle):
        """Get the closest line based on the Y value"""
        lines = []
        for _ in range(len(line_coords)):
            max_values = np.argmax(line_coords, axis=0)
            max_y_value = max(
                line_coords[max_values[1]][1], line_coords[max_values[3]][3])
            if max_y_value == line_coords[max_values[1]][1]:
                closest_line_index = max_values[1]
            else:
                closest_line_index = max_values[3]

            closest_line = line_coords.pop(closest_line_index)
            lines.append(closest_line)
            # if len(lines) > amount-1:
            #     if angle[0] >= 0:
            #         line_one_values = max(lines[0][0], lines[0][2])
            #         line_two_values = max(lines[1][0], lines[1][2])
            #     else:
            #         line_one_values = min(lines[0][0], lines[0][2])
            #         line_two_values = min(lines[1][0], lines[1][2])
            #     if ((line_one_values >= points[0][0]
            #         and line_two_values <= points[1][0]) or
            #             (line_two_values >= points[0][0] and line_one_values <= points[1][0])):
            #         break
            #     else:
            #         lines.pop(0)

        
        return lines

    def detect_parking_lines(self, image, qr_size_px, qr_size_mm, qr_distance):
        "Detect the parking lines in the image"
        qrc,  data = self.__get_qr_code_info(
            image, qr_size_px, qr_size_mm, qr_distance)
        if data['ret']:
            # display QR-code on image
            qr_code_measurements = {
                'distances': data['distances'],
                'angles': data['angles'],
                'decoded_info': data['info']}
            qrc.display(img, qr_code_measurements, verbose=2)
            qr_slope, qr_intercept = np.polyfit(
                (data['points'][0][0][0], data['points'][0][1][0]), (data['points'][0][0][1], data['points'][0][1][1]), 1)
            lines = self.get_lines(image)
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
            self.filter_lines(avg_lines, avg_lines_coords,
                             qr_slope, qr_intercept)

            # find the two closest lines to the QR-code
            lines = self.get_closest_line(avg_lines_coords, data['points'][0], 2, data['angles'])

            return lines
        return None

    def get_line_coordinates_from_parameters(self, min_x, max_x, line_parameters):
        """Get line coordinates from line parameters"""
        slope = line_parameters[0]
        intercept = line_parameters[1]
        y_1 = int(slope*min_x + intercept)
        y_2 = int(slope*max_x + intercept)
        x_1 = min_x
        x_2 = max_x
        return np.array([x_1, y_1, x_2, y_2])


if __name__ == "__main__":
    parking_slot_detector = ParkingSlotDetector(hough=[200, 5], iterations=[3, 3])
    # Tests image: 4, 7, 8
    # 4: DATA 20, 10, 50 (910 × 597)
    # 7, 8: DATA: 60, 20, 150 (880 × 495)
    img = cv2.imread('computer_vision/line_detection/assets/parking/8.png')
    copy = img.copy()
    all_lines = parking_slot_detector.get_lines(copy)
    parking_slot_detector.show_lines(copy, all_lines)

    QR_SIZE_PX = 76
    QR_SIZE_MM = 52
    QR_DISTANCE = 500
    parking_lines = parking_slot_detector.detect_parking_lines(
        img, QR_SIZE_PX, QR_SIZE_MM, QR_DISTANCE)
    parking_slot_detector.show_lines(img, parking_lines)
    cv2.imshow("original", copy)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
