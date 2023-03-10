'''Importing libraries'''
from lane_detection import LaneDetector
import cv2

def nothing(_):
    '''Empty function'''

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    avg_center_diff = []

    while True:
        CANNY_LOW_THR = 50
        CANNY_HIGH_THR = 67
        HOUGH_THRESHOLD = 80
        HOUGH_MIN_LENGTH = 500
        HOUGH_MAX_GAP = 246
        GAUSSIAN_KERNEL = 4

        lane_detector = LaneDetector(
            canny = [CANNY_LOW_THR, CANNY_HIGH_THR],
            hough = [HOUGH_THRESHOLD, HOUGH_MIN_LENGTH, HOUGH_MAX_GAP],
            blur = GAUSSIAN_KERNEL,
        )

        ret, frame = cam.read()

        all_lines = lane_detector.get_lines(frame)
        avg_lines = lane_detector.get_average_lines(all_lines)
        avg_lines = [lane_detector.get_line_coordinates_from_parameters(
            frame, line) for line in avg_lines]
        lane_detector.show_lines(frame, avg_lines)
        center_diff = lane_detector.get_diff_from_center_info(frame, avg_lines[0], avg_lines[1])
        if center_diff is not None:
            avg_center_diff.append(center_diff)
            if len(avg_center_diff) > 3:
                avg_center_diff.pop()
            cv2.putText(
                frame, f'Diff from center: {sum(avg_center_diff)/len(avg_center_diff)}', (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

        cv2.imshow('image', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
