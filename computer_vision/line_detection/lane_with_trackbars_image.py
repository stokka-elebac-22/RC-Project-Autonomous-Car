'''Importing libraries'''
from lane_detection import LaneDetector
import cv2

def nothing(_):
    '''Empty function'''

if __name__ == '__main__':
    # Trackbars
    cv2.namedWindow('Trackbars')
    cv2.createTrackbar('Canny low threshold', 'Trackbars', 100, 500, nothing)
    cv2.createTrackbar('Canny high threshold', 'Trackbars', 200, 500, nothing)
    cv2.createTrackbar('Hough threshold line length', 'Trackbars', 80, 500, nothing)
    cv2.createTrackbar('Hough minimum line length', 'Trackbars', 200, 500, nothing)
    cv2.createTrackbar('Hough maximum line gap', 'Trackbars', 300, 500, nothing)
    cv2.createTrackbar('Gaussian blur kernel size', 'Trackbars', 5, 20, nothing)

    frame = cv2.imread(
        'tests/images/lane_detection/logi/5.jpg')

    while True:
        copy = frame.copy()
        canny_low_thr = cv2.getTrackbarPos('Canny low threshold','Trackbars')
        canny_high_thr = cv2.getTrackbarPos('Canny high threshold','Trackbars')
        hough_threshold= cv2.getTrackbarPos('Hough threshold','Trackbars')
        hough_min_length = cv2.getTrackbarPos('Hough minimum line length','Trackbars')
        hough_max_gap = cv2.getTrackbarPos('Hough maximum line gap','Trackbars')
        gaussian_kernel = cv2.getTrackbarPos('Gaussian blur kernel size','Trackbars')

        lane_detector = LaneDetector(
            canny = [canny_low_thr, canny_high_thr],
            hough = [hough_threshold, hough_min_length, hough_max_gap],
            blur = gaussian_kernel,
            width=1000
        )

        all_lines = lane_detector.get_lines(copy)
        avg_lines = lane_detector.get_average_lines(all_lines)
        avg_lines = [lane_detector.get_line_coordinates_from_parameters(
            copy, line) for line in avg_lines]
        lane_detector.show_lines(copy, avg_lines)
        center_diff = lane_detector.get_diff_from_center_info(copy, avg_lines)
        if center_diff is not None:
            cv2.putText(
                copy, f'Diff from center: {center_diff}', (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

        cv2.imshow('image', copy)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("canny", canny_low_thr, canny_high_thr)
    print("hough", hough_min_length, hough_max_gap)
    print("blur", gaussian_kernel)
    cv2.destroyAllWindows()