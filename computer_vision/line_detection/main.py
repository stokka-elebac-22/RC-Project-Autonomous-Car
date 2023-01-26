"""Import needed libraries"""
import cv2
import numpy as np


class LineDetector:
    """
    DOC: Detecting lines
    """

    def __init__(self, canny: list[int, int] = None,
                 blur: int = 5,
                 hough: list[int, int] = None,
                 iterations: list[int, int] = None):
        """
        CANNY: [low_threshold, high_threshold]
        HOUGH_LINES: [min_line_length, max_line_gap]
        """
        if canny is None:
            canny = [100, 200]
        if hough is None:
            hough = [200, 30]
        if iterations is None:
            iterations = [1, 0]

        self.canny_low_thr = canny[0]
        self.canny_high_thr = canny[1]

        self.blur_kernel_size = blur

        self.hough_min_line_length = hough[0]
        self.hough_max_line_gap = hough[1]

        self.iterations = iterations

    def get_region_of_interest(self, image: np.ndarray) -> np.ndarray:
        '''
        Everything is region of interest,
        each detector type who inherits this
        can overwrite this method
        '''
        return image

    def get_lines(self, image: np.ndarray) -> np.ndarray:
        """Extract lines on the lane from image"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gaussian_blur = cv2.GaussianBlur(
            gray, (self.blur_kernel_size, self.blur_kernel_size), 0)
        canny = cv2.Canny(gaussian_blur, self.canny_low_thr,
                          self.canny_high_thr)
        dilate = cv2.dilate(canny, (3, 3), iterations=self.iterations[0])
        erode = cv2.erode(dilate, (3, 3), iterations=self.iterations[1])
        roi = self.get_region_of_interest(erode)
        lines = cv2.HoughLinesP(
            roi, 1, np.pi / 180, 40, np.array([]),
            minLineLength=self.hough_min_line_length, maxLineGap=self.hough_max_line_gap
        )
        return lines

    def show_lines(self, image: np.ndarray, lines: np.ndarray) -> None:
        """Show the lines on image"""
        if lines is not None:
            for line in lines:
                if line is not None:
                    x_1, y_1, x_2, y_2 = line.reshape(4)
                    cv2.line(image, (x_1, y_1), (x_2, y_2), (255, 0, 0), 5)


if __name__ == "__main__":
    frame = cv2.imread(
        "computer_vision/line_detection/assets/bike_park.jpg")

    SCALE_PERCENT = 30  # percent of original size
    new_width = int(frame.shape[1] * SCALE_PERCENT / 100)
    new_height = int(frame.shape[0] * SCALE_PERCENT / 100)
    dim = (new_width, new_height)

    # resize image
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    line_detector = LineDetector()

    all_lines = line_detector.get_lines(frame)
    line_detector.show_lines(frame, all_lines)
    cv2.imshow('image', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
