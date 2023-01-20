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


if __name__ == "__main__":
    parking_slot_detector = ParkingSlotDetector()
    img = cv2.imread('computer_vision/line_detection/assets/parking/1.png')

    parking_slot_detector.detect_parking_lines(img)
    lines = parking_slot_detector.get_lines(img)
    print(len(lines))
    clustered_lines = []
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
                else:
                    not_stopped = True
                    for cluster in clustered_lines:
                        for line in cluster:
                            if np.isclose((slope, intercept), cluster, rtol=1).all():
                                cluster.append((slope, intercept))
                                not_stopped = False
                                break
                    
                    if not_stopped:
                        clustered_lines.append([(slope, intercept)])
            except np.RankWarning:
                pass
    avg_lines = []
    for cluster in clustered_lines:
        line = np.average(cluster, axis=0)
        # NEED TO FIX THIS PART BELOW.. get line coordinates gives wrong coordinates
        # take average X and Y coordinates????

        # check if lines too much shorter not good dont use it
        # calculate average on coordinates each (x1,y1,x2,y2)

        coordinates = parking_slot_detector.get_line_coordinates_from_parameters(img, line)
        avg_lines.append(coordinates)
    parking_slot_detector.show_lines(img, avg_lines)
        
    #if list empty then append
    # else for each list in list check if there's relative diff okey? if yes add to that list else as new list

    # max_values = np.argmax(lines, axis=0)

    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
