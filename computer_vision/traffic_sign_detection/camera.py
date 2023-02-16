'''Importing libraries'''
from typing import TypedDict
from main import TrafficSignDetector
import cv2

SignSize = TypedDict('SignSize', {
    'px': int,
    'mm': int,
    'distance': int,
})

def nothing(_):
    '''Empty function'''

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        sign_size: SignSize = {
            'px': 10,
            'mm': 61,
            'distance': 200
        }
        traffic_sign_detection = TrafficSignDetector(sign_size)
        output_signs = traffic_sign_detection.detect_signs(frame)
        traffic_sign_detection.show_signs(frame, output_signs)

        cv2.imshow('image', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
