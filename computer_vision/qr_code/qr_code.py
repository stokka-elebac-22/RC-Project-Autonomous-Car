"""QR code module."""
import dataclasses
import cv2 as cv

@dataclasses.dataclass
class QRGeometry:
    """PointSet, used by qrcode."""
    def __init__(self, pts=None):
        if pts is None or len(pts) < 4:
            pts = [[0,0],[0,0],[0,0],[0,0]]
        self.update(pts)

    def update(self, pts):
        """update points, used by qrcode."""
        self.points = pts
        self.side_a = abs(self.points[0][0] - self.points[1][0])
        self.side_b = abs(self.points[1][1] - self.points[2][1])
        self.side_c = abs(self.points[2][0] - self.points[3][0])
        self.side_d = abs(self.points[3][1] - self.points[0][1])

class QRCode:
    """QRCode, doing calculations for QR code placement estimation."""
#                          c
#                  p2 ---------- p3
#            |             |
#         b  |             |  d
#            |             |
#            |             |
#            p1 ---------- p0
#                    a

    def __init__(self, size_px, size_mm, distance, values_length=10):
        self.ret_qr = None
        self.decoded_info = None
        self.qr_code = QRGeometry()
        self.rest = None

        self.qr_size_px = size_px
        self.qr_size_mm = size_mm
        self.qr_distance = distance

        ##### VALUES #####
        self.values_length = values_length
        self.angles = [0 for _ in range(values_length)]
        self.distance = [0 for _ in range(values_length)]

    def update(self, ret_qr, decoded_info, points, rest, resize=1):
        """Update values """
        self.ret_qr = ret_qr
        self.decoded_info = decoded_info
        self.qr_code.update(points)
        self.rest = rest
        width_px = max(abs(self.qr_code.points[0][0] - self.qr_code.points[1][0]) * (1 / resize),
        abs(self.qr_code.points[2][0] - self.qr_code.points[2][0]))
        height_px = max(abs(self.qr_code.points[2][1] - self.qr_code.points[0][1]),
        abs(self.qr_code.points[2][1] - self.qr_code.points[1][1]))

        height_px_resize = height_px * (1/resize)
        ratio = width_px/height_px

        focal_length = (self.qr_size_px / self.qr_size_mm) * self.qr_distance
        angle = (1 - ratio) * 90
        # the resize variable is only relevant if not using video
        distance = (self.qr_size_mm * focal_length) / height_px_resize
        self.filter_angle(angle)
        self.filter_distance(distance)

    def filter_angle(self, angle):
        """filter angle values """
        if angle is None:
            return
        self.angles.pop(0)
        self.angles.append(angle)

    def filter_distance(self, distance):
        """filter distance values """
        if distance is None:
            return
        self.distance.pop(0)
        self.distance.append(distance)

    def get_average_angle(self) -> int:
        """get averaged angle value """
        return sum(self.angles)//self.values_length

    def get_average_distance(self) -> int:
        """get averaged distance value """
        return sum(self.distance)//self.values_length

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

    def display(self, frame, qrc: QRCode, qrg: QRGeometry, resize=1, verbose=1):
        """Display """
        for dec_info, pts in zip(qrc.decoded_info, qrc.qr_code.points):
            if dec_info:
                color = self.color_frame_green
            else:
                color = self.color_frame_red
            frame = cv.polylines(frame, [pts.astype(int)], True, color, 4)
        if verbose > 0:
            self.display_values(frame, verbose, qrc, qrg)
        return frame

    def display_values(self, img, qrc: QRCode, qrg: QRGeometry, verbose=1):
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

            cv.putText(img, str(int(qrg.side_a)), text_location_a, self.font, \
                        self.font_scale, self.text_color, self.text_thickness, cv.LINE_AA)
            cv.putText(img, str(int(qrg.side_b)), text_location_b, self.font, \
                        self.font_scale, self.text_color, self.text_thickness, cv.LINE_AA)
            cv.putText(img, str(int(qrg.side_c)), text_location_c, self.font, \
                        self.font_scale, self.text_color, self.text_thickness, cv.LINE_AA)
            cv.putText(img, str(int(qrg.side_d)), text_location_d, self.font, \
                        self.font_scale, self.text_color, self.text_thickness, cv.LINE_AA)

        img = cv.putText(img, f'angle    = {qrc.get_average_angle()}', (10, 20), self.font, \
                            self.font_scale * 1.5, self.text_color, self.text_thickness, cv.LINE_AA)
        img = cv.putText(img, f'distance = {qrc.get_average_distance()}', (10, 50), \
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

    while True:
        frame = local_read_camera()
        ret_qr_main, decoded_info, points, rest = qcd.detectAndDecodeMulti(frame)
        if ret_qr_main:
            qr_code.update(ret_qr_main, decoded_info, points[0], rest)
            qr_code.display(frame, verbose=VERBOSE)
        cv.imshow(WINDOW_NAME, frame)
        if cv.waitKey(DELAY) & 0xFF == ord('q'):
            break
    cv.destroyWindow(WINDOW_NAME)

    # camera.run(verbose=2)
