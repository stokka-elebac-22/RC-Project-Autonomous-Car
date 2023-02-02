"""Importing necessary libraries"""
import cv2


class TrafficSignDetector:
    """
    DOC:
    """

    def __init__(self, model='computer_vision/traffic_sign_detection/stop_sign_model.xml', size_px=None, size_mm=None, distance=None):
        self.cascade = cv2.CascadeClassifier(model)
        self.sign_size_px = size_px
        self.sign_size_mm = size_mm
        self.sign_distance = distance

        if size_px is None:
            self.qr_size_px = 1
        if size_mm is None:
            self.qr_size_mm = 1
        if distance is None:
            self.qr_distance = 1

    def detect_signs(self, image):
        """Detect the signs based on the model used"""
        signs = self.cascade.detectMultiScale(image)
        return signs

    def get_distance(self, sign):
        focal_length = (self.sign_size_px / self.sign_size_mm) * self.qr_distance
        distance = (self.sign_size_mm * focal_length) / sign[3]
        return distance

    def show_signs(self, image, signs):
        """Draw the signs on the image"""
        for (x_coordinate, y_coordinate, width, height) in signs:
            cv2.rectangle(image, (x_coordinate, y_coordinate),
                          (x_coordinate+width, y_coordinate+height), (255, 0, 0), 5)


if __name__ == "__main__":

    img = cv2.imread('computer_vision/traffic_sign_detection/images/test/1.jpg')

    SCALE_PERCENT = 30  # percent of original size
    img_width = int(img.shape[1] * SCALE_PERCENT / 100)
    img_height = int(img.shape[0] * SCALE_PERCENT / 100)
    dim = (img_width, img_height)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    traffic_sign_detection = TrafficSignDetector(size_mm=61, size_px=10, distance = 200)
    output_signs = traffic_sign_detection.detect_signs(img)
    traffic_sign_detection.show_signs(img, output_signs)

    cv2.imshow('frame', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
