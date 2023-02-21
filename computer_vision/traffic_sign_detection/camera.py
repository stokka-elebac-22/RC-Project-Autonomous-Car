'''Importing libraries'''
from typing import TypedDict
import cv2
from main import TrafficSignDetector

if __name__ == '__main__':

    # define a video capture object
    cam = cv2.VideoCapture(0)

    SignSize = TypedDict('SignSize', {
        'px': int,
        'mm': int,
        'distance': int,
    })

    while True:

        ret, frame = cam.read()

        sign_size: SignSize = {
            'px': 10,
            'mm': 61,
            'distance': 200
        }
        traffic_sign_detection = TrafficSignDetector(size = sign_size)
        output_signs = traffic_sign_detection.detect_signs(frame)
        traffic_sign_detection.show_signs(frame, output_signs)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    cam.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
