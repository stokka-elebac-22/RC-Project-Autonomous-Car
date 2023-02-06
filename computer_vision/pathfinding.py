'''Main'''
from typing import TypedDict
<<<<<<< HEAD
import cv2
import pygame as pg
=======
import numpy as np
import cv2
import pygame as pg
from matplotlib import pyplot as plt
>>>>>>> 1a3835913b2785ce0df513b32b9ff1e48a3a0e1a
from pygame.locals import QUIT  # pylint: disable=no-name-in-module
try:
    from environment.src.environment import Environment
    from environment.src.display import DisplayEnvironment
    from environment.src.a_star import AStar
    from environment.src.lib import Node
    from line_detection.parking_slot_detection import ParkingSlotDetector
    from line_detection.lane_detection import LaneDetector
    from traffic_sign_detection.main import TrafficSignDetector
    from qr_code.qr_code import QRCode
except ImportError:
    from computer_vision.environment.src.environment import Environment
    from computer_vision.environment.src.display import DisplayEnvironment
    from computer_vision.environment.src.a_star import AStar
    from computer_vision.line_detection.parking_slot_detection import ParkingSlotDetector
    from computer_vision.line_detection.lane_detection import LaneDetector
    from computer_vision.traffic_sign_detection.main import TrafficSignDetector
    from computer_vision.qr_code.qr_code import QRCode
    from computer_vision.environment.src.lib import Node

def bresenham(x_0: int, y_0: int, x_1: int, y_1: int) -> list[tuple[int, int]]:
    """
    Returns a list of coordinates
    representing a line from (x1, y1) to (x2, y2)
    Source: https://github.com/encukou/bresenham
    """
    coordinates = []
    d_x = x_1 - x_0
    d_y = y_1 - y_0

    x_sign = 1 if d_x > 0 else -1
    y_sign = 1 if d_y > 0 else -1

    d_x = abs(d_x)
    d_y = abs(d_y)

    if d_x > d_y:
        x_x, x_y, y_x, y_y = x_sign, 0, 0, y_sign
    else:
        d_x, d_y = d_y, d_x
        x_x, x_y, y_x, y_y = 0, y_sign, x_sign, 0

    d_val = 2*d_y - d_x
    y_val = 0

    for x_val in range(d_x + 1):
        coordinates.append((x_0 + x_val*x_x + y_val*y_x,
                           y_0 + x_val*x_y + y_val*y_y))
        if d_val >= 0:
            y_val += 1
            d_val -= 2*d_x
        d_val += 2*d_y

    return coordinates


class PathFinding:
    '''
    Class using 2D environment mapping to calculate shortest
    path with objects that can be hindrances
    '''
    def __init__(self, size: tuple[int, int], w_size:int, pixel_width:int, pixel_height:int
                ,cam_width:int, cam_height:int, cam_center:list[int, int], object_id:int=10):
        self.ratio_width = cam_width/pixel_width
        self.ratio_height = cam_height/pixel_height
        self.size = size
        self.window_size = (w_size * (size[1]/size[0]), w_size)
        self.display = DisplayEnvironment(self.window_size, size)
        self.env = Environment(
            size, 20, {'view_point': None, 'object_id': object_id})
        self.center = cam_center
        self.a_star = AStar(weight=2, penalty=100)

    def point_to_distance(self, point:tuple[int, int]) -> tuple[int, int]:
        '''Converts point to distance'''
        offset_x = point[0] - self.center[0]/2
        offset_y = self.center[1] - point[1]
        x_distance = offset_x*self.ratio_width
        y_distance = offset_y*self.ratio_height
        return (x_distance, y_distance)

    Objects = TypedDict('Objects', {
        'points': list[tuple[int, int]],
        'distances': list[tuple[int, int]],
        'object_id': int
    })
    def insert_objects(self, objects: Objects) -> None:
        '''Insert objects into environment'''
        for groups in objects:
            coords = []
            if groups['values'] is not None:
                for group in groups['values']:
                    if groups['distance']:
                        _, coord = self.env.insert(group, groups['object_id'])
                    else:
                        distance = self.point_to_distance(group)
                        _, coord = self.env.insert(
                            distance, groups['object_id'])
                    if coord is not None:
                        coords.append(coord[0])
                        coords.append(coord[1])

                if len(coords) == 4:
                    result = bresenham(
                        coords[0], coords[1], coords[2], coords[3])
                    if result is not None:
                        for point in result:
                            self.env.insert_by_index(point, 1)


    def calculate_path(self, value: tuple[int, int], distance: bool) -> list[Node]:
        '''Calculate the shortest path to a specific point using AStar algorithm'''
        self.env.remove(12)
        if not distance:
            point = self.point_to_distance(value)
        else:
            point = value
        self.env.insert(point, 12)

        start_pos_path = self.env.get_pos(10)
        end_pos_path = self.env.get_pos(12)

        cur_mat = self.env.get_data()
        self.display.update(cur_mat)
        cur_mat = self.env.get_data()
        ret, path = self.a_star.get_data(cur_mat, start_pos_path, end_pos_path)

        if ret:
            for pos in path[1:-1]:
                self.display.insert(pos, 'Path')
        return path


if __name__ == "__main__":

    QR_SIZE_PX = 76
    QR_SIZE_MM = 52
    QR_DISTANCE = 500

    PIXEL_WIDTH = 500
    PIXEL_HEIGHT = 300
    CAM_WIDTH = 800
    CAM_HEIGHT = 500

    BOARD_SIZE = (60, 115)

    img = cv2.imread(
        'computer_vision/line_detection/assets/parking/10.png')
    center = (img.shape[1], img.shape[0])

    path_finding = PathFinding(
        BOARD_SIZE, 720, PIXEL_WIDTH, PIXEL_HEIGHT, CAM_WIDTH, CAM_HEIGHT, center)
    parking_slot_detector = ParkingSlotDetector(
        hough=[200, 5], iterations=[5, 2])
    lane_detector = LaneDetector()
    traffic_sign_detector = TrafficSignDetector(
        size_mm=61, size_px=10, distance=200)
    qr_code = QRCode(QR_SIZE_PX, QR_SIZE_MM, QR_DISTANCE)

    RUN = True
    while RUN:

        # Add hindrances using mouse
        for event in pg.event.get():
            if event.type == QUIT:
                RUN = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                TILE_SIZE = path_finding.window_size[1]/path_finding.size[0]
                col = mouse_pos[0] // TILE_SIZE
                row = mouse_pos[1] // TILE_SIZE
                path_finding.env.insert_by_index((int(row), int(col)), '1')

        # Should change this to camera frame later
        frame = cv2.imread(
            'computer_vision/line_detection/assets/parking/10.png')
        obstacles = []

        qr_data = qr_code.get_data(frame)
        if qr_data['ret']:
            distances = path_finding.point_to_distance(
                    (qr_data['points'][0][3][0]+qr_data['points'][0][2][0]/2, qr_data['points'][0][0][0]))
            qr_distance_x = distances[0]
            qr_distance_y = qr_data['distances'][0]
            obstacles.append({'values': [
                                 (qr_distance_x, qr_distance_y)],
                            'distance': True, 'object_id': 11})

        # Use ParkingSlot Module
        qr_code_data = {
            'ret': qr_data['ret'],
            'points': qr_data['points']
        }
        parking_lines = parking_slot_detector.detect_parking_lines(
            frame, qr_code_data)

        if parking_lines is not None:
            parking_lines.append(
                parking_slot_detector.get_closing_line_of_two_lines(parking_lines))
            for lines in parking_lines:
                obstacles.append({'values': [
                                 (lines[0], lines[1]), (lines[2], lines[3])],
                                 'distance': False, 'object_id': 3})

        # Use lane Module
        all_lines = lane_detector.get_lines(frame)
        avg_lines = lane_detector.get_average_lines(all_lines)
        if avg_lines is not None:
            avg_lines = [lane_detector.get_line_coordinates_from_parameters(
                frame, line) for line in avg_lines]
            for line in avg_lines:
                if line is not None:
                    obstacles.append({'values': [
                                     (line[0], line[1]), (line[2], line[3])],
                                     'distance': False, 'object_id': 4})

            center_diff = lane_detector.get_diff_from_center_info(frame, avg_lines)
            center_diff_x = 0
            center_diff_y = 0
            if center_diff is not None:
                center_diff_x = center_diff
                DESIRED_DISTANCE_FORWARD = 100
        # Use Traffic Sign module
        signs = traffic_sign_detector.detect_signs(frame)
        if signs is not None:
            for sign in signs:
                distances = path_finding.point_to_distance(
                    (sign[0]+sign[2]/2, sign[1]))
                distance_x = distances[0]
                distance_y = traffic_sign_detector.get_distance()
                obstacles.append({'values': [
                                 (distance_x, distance_y)], 'distance': True,'object_id': 5})

        path_finding.insert_objects(obstacles)
        # TODO: Test
        path = path_finding.calculate_path((460, 120), False)
        path_finding.display.display()

        # RUN = True
        # TODO: point for lane line, maybe can remove the get course functions no need?
        # path_finding.calculate_path((center_diff_x, center_diff_y), True)

        # With distance from Parking using QR!!!
        # TODO: DOES NOT WORK WHY?? maybe bcus of calibration constants
        #path_finding.calculate_path((qr_distance_x, DESIRED_DISTANCE_FORWARD), True)

        # TODO: add catmull rom spline based on points given by path
        # USE PATH variable!!!

x_values = [ point[1] for i, point in enumerate(path) if i % 5 == 0 ]
y_values = [ BOARD_SIZE[0] - (point[0] + 1) for i, point in enumerate(path) if i % 5 == 0]

def CatmullRomSpline(P0, P1, P2, P3, a, nPoints=100):
    """
    P0, P1, P2, and P3 should be (x,y) point pairs that define the Catmull-Rom spline.
    nPoints is the number of points to include in this curve segment.
    """
    # Convert the points to numpy so that we can do array multiplication
    P0, P1, P2, P3 = map(np.array, [P0, P1, P2, P3])

    # Calculate t0 to t4
    alpha = a
    def tj(ti, Pi, Pj):
        xi, yi = Pi
        xj, yj = Pj
        return ( ( (xj-xi)**2 + (yj-yi)**2 )**0.5 )**alpha + ti

    t0 = 0
    t1 = tj(t0, P0, P1)
    t2 = tj(t1, P1, P2)
    t3 = tj(t2, P2, P3)

    # Only calculate points between P1 and P2
    t = np.linspace(t1,t2,nPoints)

    # Reshape so that we can multiply by the points P0 to P3
    # and get a point for each value of t.
    t = t.reshape(len(t),1)

    A1 = (t1-t)/(t1-t0)*P0 + (t-t0)/(t1-t0)*P1
    A2 = (t2-t)/(t2-t1)*P1 + (t-t1)/(t2-t1)*P2
    A3 = (t3-t)/(t3-t2)*P2 + (t-t2)/(t3-t2)*P3

    B1 = (t2-t)/(t2-t0)*A1 + (t-t0)/(t2-t0)*A2
    B2 = (t3-t)/(t3-t1)*A2 + (t-t1)/(t3-t1)*A3

    C  = (t2-t)/(t2-t1)*B1 + (t-t1)/(t2-t1)*B2
    return C

def CatmullRomChain(P,alpha):
    """
    Calculate Catmull Rom for a chain of points and return the combined curve.
    """
    sz = len(P)

    # The curve C will contain an array of (x,y) points.
    C = []
    for i in range(sz-3):
        c = CatmullRomSpline(P[i], P[i+1], P[i+2], P[i+3],alpha)
        C.extend(c*-1)

    return C

#plt.xlim(0, BOARD_SIZE[1])
#plt.ylim(0, BOARD_SIZE[0])

a = 0.

new_path = [(value[1], value[0]) for i, value in enumerate(path) if i % 3 == 0]

c = CatmullRomChain(new_path, a)
x_values, y_values = zip(*c)
plt.plot(x_values,y_values,c='red')

plt.grid()
plt.plot(x_values, y_values, marker="o", markersize=2, markeredgecolor="red", markerfacecolor="green")
plt.show()