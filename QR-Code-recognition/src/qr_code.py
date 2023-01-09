import cv2 as cv

class Points:
    def __init__(self, points=[0, 0, 0, 0]):
        self.points = points
        self.p0 = points[0]
        self.p1 = points[1]
        self.p2 = points[2]
        self.p3 = points[3]

    def update(self, points):
        self.points = points
        points = points[0] # Because of the format from the qr code points
        self.p0 = points[0]
        self.p1 = points[1]
        self.p2 = points[2]
        self.p3 = points[3]
    
class Sides:
    def __init__(self, sides=[0, 0, 0, 0]):
        self.a = sides[0]
        self.b = sides[1]
        self.c = sides[2]
        self.d = sides[3]

    def update(self, points: Points):
        self.a = abs(points.p0[0] - points.p1[0])
        self.b = abs(points.p1[1] - points.p2[1])
        self.c = abs(points.p2[0] - points.p3[0])
        self.d = abs(points.p3[1] - points.p0[1])


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

    def display(self, frame, resize, verbose):
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
            text_location_a = (int(min(self.points.p0[0], self.points.p1[0]) + self.sides.a/2), int(self.points.p0[1]))
            text_location_b = (int(self.points.p1[0]), int(min(self.points.p1[1], self.points.p2[1]) + self.sides.b/2))
            text_location_c = (int(min(self.points.p2[0], self.points.p3[0]) + self.sides.c/2), int(self.points.p2[1]))
            text_location_d = (int(self.points.p3[0]), int(min(self.points.p3[1], self.points.p0[1]) + self.sides.d/2))

            cv.putText(frame, str(int(self.sides.a)), text_location_a, self.font, self.font_scale, self.text_color, self.text_thickness, cv.LINE_AA)
            cv.putText(frame, str(int(self.sides.b)), text_location_b, self.font, self.font_scale, self.text_color, self.text_thickness, cv.LINE_AA)
            cv.putText(frame, str(int(self.sides.c)), text_location_c, self.font, self.font_scale, self.text_color, self.text_thickness, cv.LINE_AA) 
            cv.putText(frame, str(int(self.sides.d)), text_location_d, self.font, self.font_scale, self.text_color, self.text_thickness, cv.LINE_AA)

        width_px = max(abs(self.points.p0[0] - self.points.p1[0]) * (1 / resize),
        abs(self.points.p2[0] - self.points.p3[0]))
        height_px = max(abs(self.points.p3[1] - self.points.p0[1]),
        abs(self.points.p2[1] - self.points.p1[1]))
        # width_px_resize = width_px * (1/resize)
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