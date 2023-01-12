import cv2 as cv
from camera import Camera

class Points:
    def __init__(self, points=[0, 0, 0, 0]):
        self.points = points
        self.point0 = points[0]
        self.point1 = points[1]
        self.point2 = points[2]
        self.point3 = points[3]

    def update(self, points):
        self.points = points
        self.point0 = points[0]
        self.point1 = points[1]
        self.point2 = points[2]
        self.point3 = points[3]

class Sides:
    def __init__(self, sides=[0, 0, 0, 0]):
        self.side_a = sides[0]
        self.side_b = sides[1]
        self.side_c = sides[2]
        self.side_d = sides[3]

    def update(self, points: Points):
        self.side_a = abs(points.p0[0] - points.p1[0])
        self.side_b = abs(points.p1[1] - points.p2[1])
        self.side_c = abs(points.p2[0] - points.p3[0])
        self.side_d = abs(points.p3[1] - points.p0[1])

class QRCode:
    """
                    c
            p2 ---------- p3
            |             |
         b  |             |  d
            |             |
            |             |
            p1 ---------- p0
                    a

    """
    def __init__(self, size_px, size_mm, distance, values_length=10):
        self.ret_qr = None
        self.decoded_info = None
        self.points = Points()
        self.rest = None
        self.sides = Sides()

        ##### DISPLAY #####
        self.color_frame_green = (0, 255, 0)
        self.color_frame_red = (0, 0, 255)

        self.font = cv.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.5
        self.text_color = (255, 0, 255)
        self.text_thickness = 1

        self.qr_size_px = size_px
        self.qr_size_mm = size_mm
        self.qr_distance = distance

        ##### VALUES #####
        self.values_length = values_length
        self.angles = [0 for _ in range(values_length)]
        self.distance = [0 for _ in range(values_length)]

    def update(self, ret_qr, decoded_info, points, rest):
        self.ret_qr = ret_qr
        self.decoded_info = decoded_info
        self.points.update(points)
        self.rest = rest

        self.sides.update(self.points)

    def display(self, frame, resize=1, verbose=1):
        self.display_qr_code(frame)
        if verbose > 0:
            self.display_values(frame, resize, verbose=verbose)

    def display_qr_code(self, frame):
        for s, p in zip(self.decoded_info, self.points.points):
            if s:
                color = self.color_frame_green
            else:
                color = self.color_frame_red
            frame = cv.polylines(frame, [p.astype(int)], True, color, 4)
        return frame

    def display_values(self, frame, resize=1, verbose=1):
        if verbose > 1:
            text_location_a = (int(min(self.points.point0[0], self.points.point1[0]) + self.sides.side_a/2), int(self.points.point0[1]))
            text_location_b = (int(self.points.point1[0]), int(min(self.points.point1[1], self.points.point2[1]) + self.sides.side_b/2))
            text_location_c = (int(min(self.points.point2[0], self.points.point3[0]) + self.sides.side_c/2), int(self.points.point2[1]))
            text_location_d = (int(self.points.point3[0]), int(min(self.points.point3[1], self.points.point0[1]) + self.sides.side_d/2))

            cv.putText(frame, str(int(self.sides.side_a)), text_location_a, self.font, self.font_scale, self.text_color, self.text_thickness, cv.LINE_AA)
            cv.putText(frame, str(int(self.sides.side_b)), text_location_b, self.font, self.font_scale, self.text_color, self.text_thickness, cv.LINE_AA)
            cv.putText(frame, str(int(self.sides.side_c)), text_location_c, self.font, self.font_scale, self.text_color, self.text_thickness, cv.LINE_AA)
            cv.putText(frame, str(int(self.sides.side_d)), text_location_d, self.font, self.font_scale, self.text_color, self.text_thickness, cv.LINE_AA)

        width_px = max(abs(self.points.point0[0] - self.points.point1[0]) * (1 / resize),
        abs(self.points.point2[0] - self.points.point3[0]))
        height_px = max(abs(self.points.point3[1] - self.points.point0[1]),
        abs(self.points.point2[1] - self.points.point1[1]))

        height_px_resize = height_px * (1/resize)
        ratio = width_px/height_px

        focalLength = (self.qr_size_px / self.qr_size_mm) * self.qr_distance
        angle = (1 - ratio) * 90
        distance = (self.qr_size_mm * focalLength) / height_px_resize # the resize variable is only relevant if not using video

        self.add_anlge(angle)
        self.add_distance(distance)

        frame = cv.putText(frame, f'angle    = {self.get_average_angle()}', (10, 20), self.font, self.font_scale * 1.5, self.text_color, self.text_thickness, cv.LINE_AA)
        frame = cv.putText(frame, f'distance = {self.get_average_distance()}', (10, 50), self.font, self.font_scale * 1.5, self.text_color, self.text_thickness, cv.LINE_AA)

    def add_anlge(self, angle):
        if angle is None:
            return
        self.angles.pop(0)
        self.angles.append(angle)

    def add_distance(self, distance):
        if distance is None:
            return
        self.distance.pop(0)
        self.distance.append(distance)

    def get_average_angle(self) -> int:
        return sum(self.angles)//self.values_length

    def get_average_distance(self) -> int:
        return sum(self.distance)//self.values_length


if "__main__" == __name__:
    # ----- ORIGINAL MEASUREMENTS -----
    # QR Code measured, 55mm lense
    QR_SIZE_PX = 76
    QR_SIZE_MM = 52
    QR_DISTANCE = 500
    qr_code = QRCode(QR_SIZE_PX, QR_SIZE_MM, QR_DISTANCE)
    camera = Camera()
    verbose = 1

    qcd = cv.QRCodeDetector()
    qr_code = qr_code

    while True:
        frame = camera.read()
        ret_qr, decoded_info, points, rest = qcd.detectAndDecodeMulti(frame)
        if ret_qr:
            qr_code.update(ret_qr, decoded_info, points[0], rest)
            qr_code.display(frame, verbose=verbose)
        cv.imshow(camera.window_name, frame)
        if cv.waitKey(camera.delay) & 0xFF == ord('q'):
            break
    cv.destroyWindow(camera.window_name)

    camera.run(verbose=2)