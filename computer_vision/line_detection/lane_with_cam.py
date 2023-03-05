'''Importing libraries'''
from lane_detection import LaneDetector
import cv2

def nothing(_):
    '''Empty function'''

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    avg_center_diff = []

    while True:
        canny_low_thr = 50
        canny_high_thr = 67
        hough_threshold = 80
        hough_min_length = 500
        hough_max_gap = 246
        gaussian_kernel = 4

        lane_detector = LaneDetector(
            canny = [canny_low_thr, canny_high_thr],
            hough = [hough_threshold, hough_min_length, hough_max_gap],
            blur = gaussian_kernel,
        )

        ret, frame = cam.read()

        all_lines = lane_detector.get_lines(frame)
        avg_lines = lane_detector.get_average_lines(all_lines)
        avg_lines = [lane_detector.get_line_coordinates_from_parameters(
            frame, line) for line in avg_lines]
        lane_detector.show_lines(frame, avg_lines)
        center_diff = lane_detector.get_diff_from_center_info(frame, avg_lines)
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
