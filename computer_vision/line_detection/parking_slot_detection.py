"""Import libraries"""
import warnings
import cv2
import numpy as np
from main import LineDetector


class ParkingSlotDetector(LineDetector):

    """
    DOC: Detects parking slot
    Logic behind it: Find two lines that has a qr code in between it
    Check the closest two lines

    HOW TO FIND THE AVERAGE??
    REMOVE NOISE?
    """

    def __init__(self, canny=None, blur=3, hough=None):
        '''Initialize the Line Detector'''
        LineDetector.__init__(self, canny, blur, hough)

    def detect_parking_lines(self, image):
        pass

    def get_line_coordinates_from_parameters(self, min_x, max_x, line_parameters):
        """Get line coordinates from line parameters"""
        slope = line_parameters[0]
        intercept = line_parameters[1]
        # since line will always start from bottom of image
        y_1 = int(slope*min_x + intercept)
        y_2 = int(slope*max_x + intercept)
        x_1 = min_x
        x_2 = max_x
        return np.array([x_1, y_1, x_2, y_2])


if __name__ == "__main__":
    parking_slot_detector = ParkingSlotDetector()
    img = cv2.imread('computer_vision/line_detection/assets/parking/3.png')
    copy = img.copy()
    parking_slot_detector.detect_parking_lines(img)
    lines = parking_slot_detector.get_lines(img)
    parking_slot_detector.show_lines(copy, lines)
    cv2.imshow("copy", copy)
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
                    clustered_coords.append([np.array([x_1, x_2, y_1, y_2])])
                else:
                    not_stopped = True
                    for i,cluster in enumerate(clustered_lines):
                        for j, line in enumerate(cluster):
                            # if np.isclose((slope, intercept), cluster, atol=20, rtol=1e-9).all() and np.isclose((x_1, y_1, x_2, y_2), clustered_coords[i][j], atol=500).all():
                            if np.isclose((slope, intercept), cluster, atol=30, rtol=1e-9).all():

                            # NEED TO SCALE THE DEFAULT ATOL???
                            #if np.isclose(slope, cluster[0][0], rtol=1e-9) and np.isclose(intercept, cluster[0][1], rtol=1e-9):
                                cluster.append((slope, intercept))
                                clustered_coords[i].append(np.array([x_1, x_2, y_1, y_2]))
                                not_stopped = False
                                break
                    
                    if not_stopped:
                        clustered_lines.append([(slope, intercept)])
                        clustered_coords.append([np.array([x_1, x_2, y_1, y_2])])
            except np.RankWarning:
                pass
    avg_lines = []
    for i, cluster in enumerate(clustered_lines):
        new_copy = img.copy()
        line = np.average(cluster, axis=0)
        max_values = np.argmax(clustered_coords[i], axis=0)
        max_x = np.max([clustered_coords[i][max_values[0]][0], clustered_coords[i][max_values[2]][2]])

        min_values = np.argmin(clustered_coords[i], axis=0)
        min_x = np.min([clustered_coords[i][min_values[0]][0], clustered_coords[i][min_values[2]][2]])
        
        coordinates = parking_slot_detector.get_line_coordinates_from_parameters(min_x, max_x, line)
        avg_lines.append(coordinates)
    
    lines = []
    for i in range(len(avg_lines)):
        max_values= np.argmax(avg_lines, axis=0)
        max_y = max(avg_lines[max_values[1]][1], avg_lines[max_values[3]][3])
        if max_y == avg_lines[max_values[1]][1]:
            closest_line_index = max_values[1]
        else:
            closest_line_index = max_values[3]

        closest_line = avg_lines.pop(closest_line_index)
        lines.append(closest_line)

    parking_slot_detector.show_lines(img, lines)

    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
