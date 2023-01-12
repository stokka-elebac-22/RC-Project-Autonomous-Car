import cv2
import numpy as np

import warnings

# SOURCE https://medium.com/analytics-vidhya/lane-detection-for-a-self-driving-car-using-opencv-e2aa95105b89

# NOTE:
# need to change paremeters through test and fail does not work for all images with the same parameters


def get_lane_region(image):
    offset = 250
    height = image.shape[0]
    width = image.shape[1]
    triangle = np.array(
        [[(0, height-offset), (width, height-offset),
          (int(width/2), int(height / 2.7))]]
    )
    black_image = np.zeros_like(image)
    mask = cv2.fillPoly(black_image, triangle, (255, 255, 255))
    mask = cv2.rectangle(mask, (0, height-offset),
                         (width, height), (255, 255, 255), -1)
    return cv2.bitwise_and(image, mask)


def get_line_coordinates_from_parameters(image, line_parameters):
    slope = line_parameters[0]
    intercept = line_parameters[1]
    y1 = image.shape[0]  # since line will always start from bottom of image
    y2 = int(y1 * (2.5 / 5))  # some random point at 3/5
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


def get_average_lines(image, lines):
    if lines is not None:
        left_fit = []  # will hold m,c parameters for left side lines
        right_fit = []  # will hold m,c parameters for right side lines

        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            with warnings.catch_warnings():
                warnings.filterwarnings('error')
                try:
                    parameters = np.polyfit((x1, x2), (y1, y2), 1)
                    slope = parameters[0]
                    intercept = parameters[1]
                    if slope < 0:
                        left_fit.append((slope, intercept))
                    else:
                        right_fit.append((slope, intercept))
                except np.RankWarning:
                    pass

        left_line = None
        right_line = None

        # now we have got m,c parameters for left and right line, we need to know x1,y1 x2,y2 parameters
        if len(left_fit) > 0:
            left_fit_average = np.average(left_fit, axis=0)
            left_line = get_line_coordinates_from_parameters(
                image, left_fit_average)
        if len(right_fit) > 0:
            right_fit_average = np.average(right_fit, axis=0)
            right_line = get_line_coordinates_from_parameters(
                image, right_fit_average)
        return np.array([left_line, right_line], dtype=object)
    return None


def get_lane_lines(image, kernel_size):
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gaussianBlur = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    low_treshold = 100
    high_treshold = 200
    canny = cv2.Canny(gaussianBlur, low_treshold, high_treshold)
    dilate = cv2.dilate(canny, (3, 3), iterations=1)
    roi = get_lane_region(dilate)
    lines = cv2.HoughLinesP(
        roi, 1, np.pi / 180, 40, np.array([]), minLineLength=200, maxLineGap=30
    )
    return lines


def show_lines(image, lines):
    if lines is not None:
        for line in lines:
            if line is not None:
                x1, y1, x2, y2 = line.reshape(4)
                cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 20)

def get_diff_from_center_info(image, lines):
    if lines is not None:
        width = image.shape[1]
        center_car = width/2
        center_lane = 0
        start = None
        stop = None

        real_width = 200
        for line in lines:
            if line is not None:
                x1, _, _, _ = line.reshape(4)
                if start is None:
                    start = x1
                elif stop is None:
                    stop = x1

        diff = None
        if start is not None and stop is not None:
            center_lane = start + (stop-start)/2
            diff = (center_car - center_lane)/width * real_width
        return diff


if __name__ == "__main__":
    cap = cv2.VideoCapture("./assets/challenge_video.mp4")
    frame = cv2.imread("lane_detection/assets/sykkelbane.jpg")

    scale_percent = 30  # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    while True:
        '''ret, frame = cap.read()

        if cv2.waitKey(1) == ord('q') or ret == False:
            break
        '''
        lines = get_lane_lines(frame, 5)
        lines = get_average_lines(frame, lines)
        show_lines(frame, lines)
        diff = get_diff_from_center_info(frame, lines)

        if diff is not None:
            cv2.putText(frame, f"Diff from center: {diff}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

        cv2.imshow('frame', frame)
        cv2.waitKey(0)
        break

    cap.release()
    cv2.destroyAllWindows()
