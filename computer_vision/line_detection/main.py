"""Import needed libraries"""
import cv2
import numpy as np

# NOTE:
# need to change parameters through test and fail
# does not work for all images with the same parameters


class LineDetector:
    """
    DOC: Detecting lines
    """

    def __init__(self, canny=None, blur=5, hough=None):
        """
        CANNY: [low_threshold, high_threshold, kernel_size]
        HOUGH_LINES: [min_line_length, max_line_gap]
        """
        if canny is None:
            canny = [100, 200]
        if hough is None:
            hough = [200, 30]

        self.canny_low_thr = canny[0]
        self.canny_high_thr = canny[1]

        self.blur_kernel_size = blur

        self.hough_min_line_length = hough[0]
        self.hough_max_line_gap = hough[1]

    def get_region_of_interest(self, image):
        '''
        Everything is region of interest,
        each detector type who inherits this
        can overwrite this method
        '''
        return image

    def get_line_coordinates_from_parameters(self, image, line_parameters):
        """Get line coordinates from line parameters"""
        slope = line_parameters[0]
        intercept = line_parameters[1]
        # since line will always start from bottom of image
        y_1 = image.shape[0]
        y_2 = int(y_1 * (2.3 / 5))
        x_1 = int((y_1 - intercept) / slope)
        x_2 = int((y_2 - intercept) / slope)
        return np.array([x_1, y_1, x_2, y_2])

    def get_lines(self, image):
        """Extract lines on the lane from image"""
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gaussian_blur = cv2.GaussianBlur(
            image, (self.blur_kernel_size, self.blur_kernel_size), 0)
        canny = cv2.Canny(gaussian_blur, self.canny_low_thr,
                          self.canny_high_thr)
        dilate = cv2.dilate(canny, (3, 3), iterations=1)
        roi = self.get_region_of_interest(dilate)
        lines = cv2.HoughLinesP(
            roi, 1, np.pi / 180, 40, np.array([]),
            minLineLength=self.hough_min_line_length, maxLineGap=self.hough_max_line_gap
        )
        return lines

    def show_lines(self, image, lines):
        """Show the lines on image"""
        if lines is not None:
            for line in lines:
                if line is not None:
                    x_1, y_1, x_2, y_2 = line.reshape(4)
                    cv2.line(image, (x_1, y_1), (x_2, y_2), (255, 0, 0), 5)


if __name__ == "__main__":
    # cap = cv2.VideoCapture("./assets/challenge_video.mp4")
    frame = cv2.imread(
        "computer_vision/line_detection/assets/bike_park.jpg")

    SCALE_PERCENT = 30  # percent of original size
    new_width = int(frame.shape[1] * SCALE_PERCENT / 100)
    new_height = int(frame.shape[0] * SCALE_PERCENT / 100)
    dim = (new_width, new_height)

    # resize image
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    line_detector = LineDetector()

    while True:
        # ret, frame = cap.read()
        # if cv2.waitKey(1) == ord('q') or ret == False:
        #    break
        all_lines = line_detector.get_lines(frame)
        line_detector.show_lines(frame, all_lines)
        cv2.imshow('image', frame)

        # cv2.imshow('frame', frame)
        cv2.waitKey(0)
        break

    # cap.release()
    cv2.destroyAllWindows()
