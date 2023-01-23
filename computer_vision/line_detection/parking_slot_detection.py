"""Import libraries"""
from qr_code.qr_code import QRCode
import warnings
import cv2
import numpy as np
from main import LineDetector
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


class ParkingSlotDetector(LineDetector):

    """
    DOC: Detects parking slot
    """

    def __init__(self, canny=None, blur=3, hough=None):
        '''Initialize the Line Detector'''
        LineDetector.__init__(self, canny, blur, hough)

    def detect_parking_lines(self, image):
        QR_SIZE_PX = 76
        QR_SIZE_MM = 52
        QR_DISTANCE = 500
        qr_code = QRCode(QR_SIZE_PX, QR_SIZE_MM, QR_DISTANCE)
        retval, distance, angle, decoded_info, points, _ = qr_code.get_data(
            img)
        if retval:
            qr_code.display(img, angle, distance, decoded_info)

            qr_slope, qr_intercept = np.polyfit(points[0][0], points[0][1], 1)
            lines = self.get_lines(image)
            if lines is None:
                return None
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
                            for i, cluster in enumerate(clustered_lines):
                                for line in cluster:
                                    if np.isclose((slope, intercept), cluster, atol=20, rtol=1e-9).all():
                                        cluster.append((slope, intercept))
                                        clustered_coords[i].append(
                                            np.array([x_1, y_1, x_2, y_2]))
                                        not_stopped = False
                                        break

                            if not_stopped:
                                clustered_lines.append([(slope, intercept)])
                                clustered_coords.append(
                                    [np.array([x_1, y_1, x_2, y_2])])
                    except np.RankWarning:
                        pass

            avg_lines_coords = []
            avg_lines = []
            for i, cluster in enumerate(clustered_lines):
                line = np.average(cluster, axis=0)
                avg_lines.append(line)
                max_values = np.argmax(clustered_coords[i], axis=0)
                max_x = np.max([clustered_coords[i][max_values[0]]
                               [0], clustered_coords[i][max_values[2]][2]])
                min_values = np.argmin(clustered_coords[i], axis=0)
                min_x = np.min([clustered_coords[i][min_values[0]]
                               [0], clustered_coords[i][min_values[2]][2]])
                coordinates = parking_slot_detector.get_line_coordinates_from_parameters(
                    min_x, max_x, line)
                avg_lines_coords.append(coordinates)

            for i, line in enumerate(avg_lines):
                # intercept atol = 20 ok for picture 7 and 8 but not for picture 4 need it for 150
                if np.isclose(qr_slope, line[0], atol=20, rtol=1e-9) and np.isclose(qr_intercept, line[1], atol=50, rtol=1e-9):
                    avg_lines.pop(i)
                    avg_lines_coords.pop(i)

            # TODO: might not need this, detect check coordinates with QR-codes
            lines = []
            for i in range(len(avg_lines_coords)):
                max_values = np.argmax(avg_lines_coords, axis=0)
                max_y = max(
                    avg_lines_coords[max_values[1]][1], avg_lines_coords[max_values[3]][3])
                if max_y == avg_lines_coords[max_values[1]][1]:
                    closest_line_index = max_values[1]
                else:
                    closest_line_index = max_values[3]

                closest_line = avg_lines_coords.pop(closest_line_index)
                lines.append(closest_line)

                if len(lines) > 1:
                    if ((max(lines[0][0], lines[0][2]) >= points[0][0][0] and max(lines[1][0], lines[1][2]) <= points[0][1][0]) or
                            (max(lines[1][0], lines[1][2]) >= points[0][0][0] and max(
                                lines[0][0], lines[0][2]) <= points[0][1][0])
                            ):
                        break
                    else:
                        lines.pop(0)

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
    parking_slot_detector = ParkingSlotDetector(hough=[200, 5])

    # Tests image: 4, 7, 8
    # 4: DATA 20, 10, 50 (910 × 597)
    # 7, 8: DATA: 60, 20, 150 (880 × 495)
    img = cv2.imread('computer_vision/line_detection/assets/parking/8.png')
    copy = img.copy()
    all_lines = parking_slot_detector.get_lines(copy)
    parking_slot_detector.show_lines(copy, all_lines)
    parking_lines = parking_slot_detector.detect_parking_lines(img)
    parking_slot_detector.show_lines(img, parking_lines)
    cv2.imshow("original", copy)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
