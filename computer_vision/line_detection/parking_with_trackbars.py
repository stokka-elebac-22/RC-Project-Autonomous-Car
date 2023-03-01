'''Importing libraries'''
import os
import sys
from parking_slot_detection import ParkingSlotDetector
import cv2

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from qr_code.qr_code import QRCode

def nothing(_):
    '''Empty function'''

if __name__ == "__main__":
    cam = cv2.VideoCapture(1)

    # Global Constants
    QR_SIZE_PX = 76
    QR_SIZE_MM = 52
    QR_DISTANCE = 500
    qr_size = {
        'px': 76,
        'mm': 52,
        'distance': 500
    }
    qr_code = QRCode(size=qr_size)

    # Trackbars
    cv2.namedWindow('Trackbars')
    cv2.createTrackbar('Canny low threshold', 'Trackbars', 100, 500, nothing)
    cv2.createTrackbar('Canny high threshold', 'Trackbars', 200, 500, nothing)
    cv2.createTrackbar('Hough minimum line length', 'Trackbars', 200, 500, nothing)
    cv2.createTrackbar('Hough maximum line gap', 'Trackbars', 300, 500, nothing)
    cv2.createTrackbar('Gaussian blur kernel size', 'Trackbars', 5, 20, nothing)
    cv2.createTrackbar('Dilate iterations', 'Trackbars', 1, 20, nothing)
    cv2.createTrackbar('Erode iterations', 'Trackbars', 0, 20, nothing)
    cv2.createTrackbar('Filter atol slope', 'Trackbars', 20, 20, nothing)
    cv2.createTrackbar('Filter atol intercept', 'Trackbars', 20, 20, nothing)
    cv2.createTrackbar('Cluster atol', 'Trackbars', 5, 20, nothing)

    while True:
        canny_low_thr = cv2.getTrackbarPos('Canny low threshold','Trackbars')
        canny_high_thr = cv2.getTrackbarPos('Canny high threshold','Trackbars')
        hough_min_length = cv2.getTrackbarPos('Hough minimum line length','Trackbars')
        hough_max_gap = cv2.getTrackbarPos('Hough maximum line gap','Trackbars')
        gaussian_kernel = cv2.getTrackbarPos('Gaussian blur kernel size','Trackbars')
        dilate_iter = cv2.getTrackbarPos('Dilate iterations','Trackbars')
        erode_iter = cv2.getTrackbarPos('Erode iterations','Trackbars')
        filter_atol_slope = cv2.getTrackbarPos('Filter atol intercept','Trackbars')
        filter_atol_intercept = cv2.getTrackbarPos('Filter atol intercept','Trackbars')
        cluster_atol = cv2.getTrackbarPos('Cluster atol','Trackbars')

        parking_slot_detector = ParkingSlotDetector(
            canny = [canny_low_thr, canny_high_thr],
            hough = [hough_min_length, hough_max_gap],
            blur = gaussian_kernel,
            iterations=[dilate_iter, erode_iter],
            filter_atol=[filter_atol_slope, filter_atol_intercept],
            cluster_atol = cluster_atol
        )

        ret, frame = cam.read()

        # Commented this out, because it did not work. Need to call it correctly

        data = qr_code.get_data(frame)
        qr_code_data = {
            'ret': data['ret'],
            'points': data['points']
        }
        print(data['ret'])
        parking_lines = parking_slot_detector.get_parking_slot(
            frame, qr_code_data)
        parking_slot_detector.show_lines(frame, parking_lines)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("canny", canny_low_thr, canny_high_thr)
    print("hough", hough_min_length, hough_max_gap)
    print("blur", gaussian_kernel)
    print("iter", dilate_iter, erode_iter)
    print("filter", filter_atol_slope, filter_atol_intercept)
    print("cluter", cluster_atol)
    cam.release()
    cv2.destroyAllWindows()
