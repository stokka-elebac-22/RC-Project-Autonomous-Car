"""QR code module."""
import dataclasses
import cv2 as cv

@dataclasses.dataclass
class QRGeometry:
    """PointSet, used by qrcode."""
    def __init__(self, pts=None):
        if pts is None or len(pts[0]) < 4:
            pts = [[[0,0],[0,0],[0,0],[0,0]]]
        self.update(pts)

    def update(self, pts):
        """update points, used by qrcode."""
        self.points = pts[0]
        self.side_a = abs(self.points[0][0] - self.points[1][0])
        self.side_b = abs(self.points[1][1] - self.points[2][1])
        self.side_c = abs(self.points[2][0] - self.points[3][0])
        self.side_d = abs(self.points[3][1] - self.points[0][1])

class QRCode:
    """QRCode, doing calculations for QR code placement estimation."""
#                          c
#            p2 ---------- p3
#            |             |
#         b  |             |  d
#            |             |
#            |             |
#            p1 ---------- p0
#                    a

    def __init__(self, size_px, size_mm, distance):
        self.qr_size_px = size_px
        self.qr_size_mm = size_mm
        self.qr_distance = distance

    def get_measurements(self, frame, resize=1):
        """Update values
        The resize variable is only relevant if not using video
        This function returns:
        - bool, stating if it could detect the qr code
        - a float value for distance and angle
        - a list of points (formatted like [[[0, 0], ..., [1, 1]]])
        - return straight value
        get_measurements(self, frame, resize=1) -> bool, float, float
        """
        qcd = cv.QRCodeDetector()
        ret_qr, _ , points_qr, rest_qr = qcd.detectAndDecodeMulti(frame)
        if not ret_qr:
            return False, None, None, None, None
        width_px = max(abs(points_qr[0][0] - points_qr[1][0]) * (1 / resize),
        abs(points_qr[2][0] - points_qr[2][0]))
        height_px = max(abs(points_qr[2][1] - points_qr[0][1]),
        abs(points_qr[2][1] - points_qr[1][1]))

        height_px_resize = height_px * (1/resize)
        ratio = width_px/height_px

        focal_length = (self.qr_size_px / self.qr_size_mm) * self.qr_distance
        angle = (1 - ratio) * 90
        distance = (self.qr_size_mm * focal_length) / height_px_resize
        return True, distance, angle, points_qr, rest_qr
class DisplayQRCode:
    """DisplayQRCode, QR code placement estimation."""
    def __init__(self):
        ##### DISPLAY #####
        self.color_frame_green = (0, 255, 0)
        self.color_frame_red = (0, 0, 255)

        self.font = cv.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.5
        self.text_color = (255, 0, 255)
        self.text_thickness = 1

    def display(self, frame, qrc: QRCode, angle: int, dist, verbose=1):
        """
        Display
        returns a frame
        """
        if qrc.decoded_info:
            color = self.color_frame_green
        else:
            color = self.color_frame_red
        frame = cv.polylines(frame, [qrc.qrg.points.astype(int)], True, color, 4)
        if verbose > 0:
            self.display_values(frame, qrc, qrc.qrg, angle, dist, verbose)
        return frame

    def display_values(self, frame, qrg: QRGeometry, angle: int, dist: int, verbose=1):
        """Display values"""
        if verbose > 1:
            text_location_a = (int(min(qrg.points[0][0], qrg.points[1][0]) + \
                                    qrg.side_a/2), int(qrg.points[0][1]))
            text_location_b = (int(qrg.points[1][0]), int(min(qrg.points[1][1], \
                                    qrg.points[2][1]) + qrg.side_b/2))
            text_location_c = (int(min(qrg.points[2][0], qrg.points[2][0]) + \
                                    qrg.side_c/2), int(qrg.points[2][1]))
            text_location_d = (int(qrg.points[2][0]), int(min(qrg.points[2][1], \
                                    qrg.points[0][1]) + qrg.side_d/2))

            cv.putText(frame, str(int(qrg.side_a)), text_location_a, self.font, \
                        self.font_scale, self.text_color, self.text_thickness, cv.LINE_AA)
            cv.putText(frame, str(int(qrg.side_b)), text_location_b, self.font, \
                        self.font_scale, self.text_color, self.text_thickness, cv.LINE_AA)
            cv.putText(frame, str(int(qrg.side_c)), text_location_c, self.font, \
                        self.font_scale, self.text_color, self.text_thickness, cv.LINE_AA)
            cv.putText(frame, str(int(qrg.side_d)), text_location_d, self.font, \
                        self.font_scale, self.text_color, self.text_thickness, cv.LINE_AA)

        cv.putText(frame, f'angle    = {angle}', (10, 20), self.font, \
                            self.font_scale * 1.5, self.text_color, self.text_thickness, cv.LINE_AA)
        cv.putText(frame, f'distance = {distance}', (10, 50), \
                self.font, self.font_scale * 1.5, self.text_color, self.text_thickness, cv.LINE_AA)

def local_read_camera(name=None, resize=1):
    """Local read camera """
    if not name:
        ret, frame = cap.read()
        if not ret:
            raise SystemError
    else:
        frame = cv.imread(name)
    frame = cv.resize(frame, (0, 0), fx = resize, fy = resize)
    return frame


if __name__ == '__main__':
    # ----- ORIGINAL MEASUREMENTS -----
    # QR Code measured, 55mm lense
    QR_SIZE_PX = 76
    QR_SIZE_MM = 52
    QR_DISTANCE = 500
    qr_code = QRCode(QR_SIZE_PX, QR_SIZE_MM, QR_DISTANCE)
    CAMERA_ID = 0
    DELAY = 1
    WINDOW_NAME = 'window'
    cap = cv.VideoCapture(CAMERA_ID)
    VERBOSE = 1

    qcd = cv.QRCodeDetector()

    qr_code_display = DisplayQRCode()

    ##### VALUES #####
    VALUES_LENGTH = 10
    angles = [0 for _ in range(VALUES_LENGTH)]
    distance = [0 for _ in range(VALUES_LENGTH)]

    def filter_angle(angle):
        """filter angle values """
        if angle is None:
            return
        angles.pop(0)
        angles.append(angle)

    def filter_distance(distance):
        """filter distance values """
        if distance is None:
            return
        distance.pop(0)
        distance.append(distance)

    qrg = QRGeometry()

    while True:
        img = local_read_camera()
        retval, distance, angle, points, rest = qr_code.get_measurements(img)
        filter_angle(angle)
        filter_distance(distance)
        if retval:
            qrg.update(points)
            average_angle = sum(angles)//VALUES_LENGTH
            average_distance = sum(distance)//VALUES_LENGTH
            qr_code_display.display(img, qrg, average_angle, average_distance)
        cv.imshow(WINDOW_NAME, img)
        if cv.waitKey(DELAY) & 0xFF == ord('q'):
            break
    cv.destroyWindow(WINDOW_NAME)

    # camera.run(verbose=2)
