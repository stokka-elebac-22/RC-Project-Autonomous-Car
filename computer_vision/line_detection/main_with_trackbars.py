'''Import libraries'''
from line_detector import LineDetector
import cv2

def nothing(_):
    '''Empty function'''

if __name__ == "__main__":
    cam = cv2.VideoCapture(0)

    # Trackbars
    cv2.namedWindow('Trackbars')
    cv2.createTrackbar('Canny low threshold', 'Trackbars', 100, 500, nothing)
    cv2.createTrackbar('Canny high threshold', 'Trackbars', 200, 500, nothing)
    cv2.createTrackbar('Hough minimum line length', 'Trackbars', 200, 500, nothing)
    cv2.createTrackbar('Hough maximum line gap', 'Trackbars', 300, 500, nothing)
    cv2.createTrackbar('Gaussian blur kernel size', 'Trackbars', 5, 20, nothing)
    cv2.createTrackbar('Dilate iterations', 'Trackbars', 1, 20, nothing)
    cv2.createTrackbar('Erode iterations', 'Trackbars', 0, 20, nothing)

    while True:
        canny_low_thr = cv2.getTrackbarPos('Canny low threshold','Trackbars')
        canny_high_thr = cv2.getTrackbarPos('Canny high threshold','Trackbars')
        hough_min_length = cv2.getTrackbarPos('Hough minimum line length','Trackbars')
        hough_max_gap = cv2.getTrackbarPos('Hough maximum line gap','Trackbars')
        gaussian_kernel = cv2.getTrackbarPos('Gaussian blur kernel size','Trackbars')
        dilate_iter = cv2.getTrackbarPos('Dilate iterations','Trackbars')
        erode_iter = cv2.getTrackbarPos('Erode iterations','Trackbars')

        line_detector = LineDetector(
            canny = [canny_low_thr, canny_high_thr],
            hough = [hough_min_length, hough_max_gap],
            blur = gaussian_kernel,
            iterations=[dilate_iter, erode_iter]
        )

        ret, frame = cam.read()

        all_lines = line_detector.get_lines(frame)
        line_detector.show_lines(frame, all_lines)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
