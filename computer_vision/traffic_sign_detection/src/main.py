"""Importing necessary libraries"""
import cv2


class TrafficSignDetector:
    """
    DOC:
    """

    def __init__(self, model='computer_vision/traffic_sign_detection/stop_sign_model.xml'):
        self.cascade = cv2.CascadeClassifier(model)

    def detect_signs(self, image):
        """Detect the signs based on the model used"""
        signs = self.cascade.detectMultiScale(image)
        return signs

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

    traffic_sign_detection = TrafficSignDetector()
    output_signs = traffic_sign_detection.detect_signs(img)
    traffic_sign_detection.show_signs(img, output_signs)

    cv2.imshow('frame', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
