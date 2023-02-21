"""Importing necessary libraries"""
import cv2
from typing import TypedDict

SignSize = TypedDict('SignSize', {
    'px': int,
    'mm': int,
    'distance': int,
})

class TrafficSignDetector:
    """
    DOC:
    """
    
    def __init__(
            self,
            model='computer_vision/traffic_sign_detection/stop_sign_model.xml',
            size: SignSize=None):
        self.cascade = cv2.CascadeClassifier(model)

        if size is None:
            self.size = {}
        else:
            self.size = size

        if self.size.get('px') is None:
            self.size['px'] = 1
        if self.size.get('mm') is None:
            self.size['mm'] = 1
        if self.size.get('distance') is None:
            self.size['distance'] = 1
        
    def detect_signs(self, image):
        '''Detect the signs based on the model used'''
        signs = self.cascade.detectMultiScale(image)
        return signs

    def get_distance(self, sign):
        '''Get distance'''
        focal_length = (self.size['px'] / self.size['mm']) * self.size['distance']
        distance = (self.size['mm']* focal_length) / sign[3]
        return distance

    def show_signs(self, image, signs):
        '''Draw the signs on the image'''
        for (x_coordinate, y_coordinate, width, height) in signs:
            cv2.rectangle(image, (x_coordinate, y_coordinate),
                          (x_coordinate+width, y_coordinate+height), (255, 0, 0), 5)



if __name__ == '__main__':
    img = cv2.imread('computer_vision/traffic_sign_detection/images/test/1.jpg')

    SCALE_PERCENT = 30  # percent of original size
    img_width = int(img.shape[1] * SCALE_PERCENT / 100)
    img_height = int(img.shape[0] * SCALE_PERCENT / 100)
    dim = (img_width, img_height)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    sign_size: SignSize = {
        'px': 10,
        'mm': 61,
        'distance': 200
    }
    traffic_sign_detection = TrafficSignDetector(size=sign_size)
    output_signs = traffic_sign_detection.detect_signs(img)
    traffic_sign_detection.show_signs(img, output_signs)

    cv2.imshow('frame', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
