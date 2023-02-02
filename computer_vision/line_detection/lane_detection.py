"""Import libraries"""
from typing import TypedDict
import warnings
import cv2
import numpy as np
try:
    from computer_vision.line_detection.main import LineDetector
except ImportError:
    try:
        from line_detection.main import LineDetector
    except ImportError:
        from main import LineDetector

# SOURCE
# https://medium.com/analytics-vidhya/lane-detection-for-a-self-driving-car-using-opencv-e2aa95105b89

class LaneDetector(LineDetector):
    """
    DOC: Detects driving lane
    """

    def __init__(self, canny: list[int, int] = None, blur: int = 5, hough: list[int, int] = None):
        '''Initialize the Line Detector'''
        LineDetector.__init__(self, canny, blur, hough)

    def get_region_of_interest(self, image: np.ndarray) -> np.ndarray:
        """Get the region of interest from image"""
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

    def get_line_coordinates_from_parameters(self, image: np.ndarray,
                                             line_parameters: list[float, float]) -> np.ndarray:
        """Get line coordinates from line parameters"""
        if line_parameters is None:
            return None
        slope = line_parameters[0]
        intercept = line_parameters[1]
        # since line will always start from bottom of image
        y_1 = image.shape[0]
        y_2 = int(y_1 * (2.3 / 5))
        x_1 = int((y_1 - intercept) / slope)
        x_2 = int((y_2 - intercept) / slope)
        return np.array([x_1, y_1, x_2, y_2])

    def get_average_lines(self, lines: np.ndarray) -> np.ndarray:
        """Sort the lines into left and right and get the average for each side"""
        if lines is not None:
            left_fit = []  # will hold intercept and slope parameters for the left side lines
            right_fit = []  # will hold intercept and slope parameters for the right side lines

            for line in lines:
                x_1, y_1, x_2, y_2 = line.reshape(4)
                with warnings.catch_warnings():
                    warnings.filterwarnings('error')
                    try:
                        parameters = np.polyfit((x_1, x_2), (y_1, y_2), 1)
                        slope = parameters[0]
                        intercept = parameters[1]
                        if slope < 0:
                            left_fit.append((slope, intercept))
                        else:
                            right_fit.append((slope, intercept))
                    except np.RankWarning:
                        pass

            # now we have got m,c parameters for left and right line,
            # we need to know x1,y1 x2,y2 parameters
            left_fit_average = None
            right_fit_average = None
            if len(left_fit) > 0:
                left_fit_average = np.average(left_fit, axis=0)
            if len(right_fit) > 0:
                right_fit_average = np.average(right_fit, axis=0)
            return np.array([left_fit_average, right_fit_average], dtype=object)
        return np.array([None, None])

    def get_diff_from_center_info(self, image: np.ndarray, lines: np.ndarray) -> float:
        """Calculate the difference from car center to lane center"""
        if lines is not None:
            width = image.shape[1]
            center_car = width/2
            center_lane = 0
            start = None
            stop = None

            real_width = 200
            for line in lines:
                if line is not None:
                    x_1, _, _, _ = line.reshape(4)
                    if start is None:
                        start = x_1
                    elif stop is None:
                        stop = x_1

            diff = None
            if start is not None and stop is not None:
                center_lane = start + (stop-start)/2
                diff = (center_car - center_lane)/width * real_width
            return diff

    CirclePoints = list[tuple[int, int], tuple[int, int], tuple[int, int]]
    CoursePolys = list[list[float, float], list[float, float]]
    CourseData = TypedDict('CourseData', {
        'warped_shape': np.ndarray,
        'perspective_transform': np.ndarray,
        'points': CirclePoints,
        'polys': CoursePolys
    })

    def get_course(self, image: np.ndarray, lines: np.ndarray) -> CourseData:
        """Returns polys that define the course and points used to define the polys"""
        if lines is None:
            return (None, None, None, None)
        if lines[0] is None or lines[1] is None:
            return (None, None, None, None)
        coordinates_x = [lines[0][0], lines[1][0]]
        # coordinates_y = [points_coordinates[0][3], points_coordinates[1][3]]
        width = max(coordinates_x) - min(coordinates_x)

        # TODO: need to change size here, measure in real life
        height = image.shape[0]

        offset = int(image.shape[1]/2 - min(coordinates_x))

        pt_output = np.float32([[0, 0],
                                [0, height],
                                [width, height],
                                [width, 0]])

        pt_input = np.float32([[lines[0][2], lines[0][3]],
                               [lines[0][0], lines[0][1]],
                               [lines[1][0], lines[1][1]],
                               [lines[1][2], lines[1][3]]])

        perspective_transform = cv2.getPerspectiveTransform(
            pt_input, pt_output)

        warped = cv2.warpPerspective(
            image, perspective_transform, (width, height), flags=cv2.INTER_LINEAR)

        x_1 = offset
        y_1 = warped.shape[0]

        x_3 = int(warped.shape[1]/2)
        y_3 = int(warped.shape[0]*0.6)

        x_2 = int(offset + (x_3 - offset)/2)
        y_2 = int(y_3 + (warped.shape[0]-y_3)/2)

        poly_1 = np.polyfit([x_1, x_2, x_3], [y_1, y_2, y_1], 2)

        poly_2 = np.polyfit([x_1, x_2, x_3], [y_3, y_2, y_3,], 2)

        data = {
            "warped_shape": warped.shape,
            "perspective_transform": perspective_transform,
            "points": [(x_1, y_1), (x_2, y_2), (x_3, y_3)],
            "polys": [poly_1, poly_2]
        }

        return data

    CourseImages = TypedDict('CourseImages', {
        'warped': np.ndarray,
        'weighted': np.ndarray
    })

    def show_course(self, image: np.ndarray,
                    warped_shape: np.ndarray,
                    circle_points: CirclePoints,
                    perspective_transform: np.ndarray,
                    polys: CoursePolys) -> CourseImages:
        """Display the points and curves for the driving course"""
        x_1 = circle_points[0][0]
        x_2 = circle_points[1][0]
        x_3 = circle_points[2][0]
        y_1 = circle_points[0][1]
        y_2 = circle_points[1][1]
        y_3 = circle_points[2][1]

        warped = cv2.warpPerspective(
            image, perspective_transform, (warped_shape[1],
                                           warped_shape[0]), flags=cv2.INTER_LINEAR)

        cv2.line(warped, (x_3, y_1), (x_3, 0), (255, 255, 0), 20)

        linear_space_1 = np.linspace(x_1, x_2, 100)
        linear_space_2 = np.linspace(x_2, x_3, 100)
        linear_spaces = [linear_space_1, linear_space_2]

        for i, _ in enumerate(linear_spaces):
            draw_x = linear_spaces[i]
            draw_y = np.polyval(polys[i], draw_x)
            draw_points = (np.asarray([draw_x, draw_y]).T).astype(
                np.int32)
            cv2.polylines(warped, [draw_points], False, (0, 0, 0), 15)

        cv2.circle(
            warped, (x_1, y_1), 10, (0, 0, 255), 20)
        cv2.circle(
            warped, (x_3, y_1), 10, (255, 0, 0), 20)
        cv2.circle(
            warped, (x_3, y_3), 10, (255, 0, 0), 20)
        cv2.circle(
            warped, (x_2, y_2), 10, (0, 255, 0), 20)

        un_warped = cv2.warpPerspective(warped, np.linalg.inv(
            perspective_transform), (image.shape[1], image.shape[0]), cv2.BORDER_TRANSPARENT)

        weighted = cv2.addWeighted(image, 0.4, un_warped, 0.2, 0)

        data = {
            'warped': warped,
            'weighted': weighted
        }

        return data


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

    lane_detector = LaneDetector()

    while True:
        # ret, frame = cap.read()
        # if cv2.waitKey(1) == ord('q') or ret == False:
        #    break
        all_lines = lane_detector.get_lines(frame)
        avg_lines = lane_detector.get_average_lines(all_lines)
        avg_lines = [lane_detector.get_line_coordinates_from_parameters(
            frame, line) for line in avg_lines]
        lane_detector.show_lines(frame, avg_lines)
        center_diff = lane_detector.get_diff_from_center_info(frame, avg_lines)
        if center_diff is not None:
            cv2.putText(
                frame, f"Diff from center: {center_diff}", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

        course_data = lane_detector.get_course(
            frame, avg_lines)

        NO_NONE = True

        for key, value in course_data.items():
            if value is None:
                NO_NONE = False
                break

        if NO_NONE:
            images = lane_detector.show_course(
                    frame,
                    course_data['warped_shape'],
                    course_data['points'],
                    course_data['perspective_transform'],
                    course_data['polys']
                )
            cv2.imshow('warped', images['warped'])
            cv2.imshow('course', images['weighted'])
        cv2.imshow('image', frame)

        # cv2.imshow('frame', frame)
        cv2.waitKey(0)
        break

    # cap.release()
    cv2.destroyAllWindows()
