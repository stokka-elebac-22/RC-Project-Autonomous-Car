'''Main'''
import cv2
import pygame as pg
from pygame.locals import QUIT  # pylint: disable=no-name-in-module
from environment.src.environment import Environment
from environment.src.display import DisplayEnvironment
from environment.src.a_star import AStar
from line_detection.parking_slot_detection import ParkingSlotDetector
from line_detection.lane_detection import LaneDetector
from traffic_sign_detection.main import TrafficSignDetector

def bresenham(x_0, y_0, x_1, y_1):
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

    def __init__(self, size, w_size, pixel_width, pixel_height
                ,cam_width, cam_height, cam_center, object_id=10):
        self.ratio_width = cam_width/pixel_width
        self.ratio_height = cam_height/pixel_height
        self.size = size
        self.window_size = (w_size * (size[1]/size[0]), w_size)
        self.display = DisplayEnvironment(self.window_size, size)
        self.env = Environment(
            size, 20, {'view_point': None, 'object_id': object_id})
        self.center = cam_center
        self.a_star = AStar(weight=10, penalty=1)

    def point_to_distance(self, point):
        '''Converts point to distance'''
        offset_x = point[0] - self.center[0]/2
        offset_y = self.center[1] - point[1]
        x_distance = offset_x*self.ratio_width
        y_distance = offset_y*self.ratio_height
        return (x_distance, y_distance)

    def insert_objects(self, objects):
        '''Insert objects into environment'''
        for groups in objects:
            coords = []
            if groups['points'] is not None:
                for group in groups['points']:
                    _, coord = self.env.insert(
                        self.point_to_distance(group), groups['object_id'])
                    if coord is not None:
                        coords.append(coord[0])
                        coords.append(coord[1])

                if len(coords) == 4:
                    result = bresenham(
                        coords[0], coords[1], coords[2], coords[3])
                    if result is not None:
                        for point in result:
                            self.env.insert_by_index(point, 1)

            coords = []
            if groups['distances'] is not None:
                for group in groups['distances']:
                    _, coord = self.env.insert(group, groups['object_id'])
                    if coord is not None:
                        coords.append(coord[0])
                        coords.append(coord[1])

                if len(coords) == 4:
                    result = bresenham(
                        coords[0], coords[1], coords[2], coords[3])
                    if result is not None:
                        for point in result:
                            self.env.insert_by_index(point, 1)

    def calculate_path(self, point):
        '''Calculate the shortest path to a specific point using AStar algorithm'''
        self.env.remove(12)
        converted_point = self.point_to_distance(point)
        self.env.insert(converted_point, 12)

        start_pos_path = self.env.get_pos(10)
        end_pos_path = self.env.get_pos(12)

        cur_mat = self.env.get_data()
        self.display.update(cur_mat)
        cur_mat = self.env.get_data()
        ret, path = self.a_star.get_data(cur_mat, start_pos_path, end_pos_path)

        if ret:
            for pos in path[1:-1]:
                self.display.insert(pos, 'Path')

        self.display.display()


if __name__ == "__main__":

    QR_SIZE_PX = 76
    QR_SIZE_MM = 52
    QR_DISTANCE = 500

    PIXEL_WIDTH = 500
    PIXEL_HEIGHT = 300
    CAM_WIDTH = 800
    CAM_HEIGHT = 500

    img = cv2.imread(
        'computer_vision/line_detection/assets/parking/10.png')
    center = (img.shape[1], img.shape[0])

    path_finding = PathFinding(
        (60, 115), 720, PIXEL_WIDTH, PIXEL_HEIGHT, CAM_WIDTH, CAM_HEIGHT, center)
    parking_slot_detector = ParkingSlotDetector(
        hough=[200, 5], iterations=[5, 2])
    lane_detector = LaneDetector()
    traffic_sign_detector = TrafficSignDetector(
        size_mm=61, size_px=10, distance=200)

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

        # Use ParkingSlot Module
        parking_lines = parking_slot_detector.detect_parking_lines(
            frame, QR_SIZE_PX, QR_SIZE_MM, QR_DISTANCE)

        if parking_lines is not None:
            parking_lines.append(
                parking_slot_detector.get_closing_line_of_two_lines(parking_lines))
            for lines in parking_lines:
                obstacles.append({'points': [
                                 (lines[0], lines[1]), (lines[2], lines[3])],
                                 'distances': None, 'object_id': 3})

        # Use lane Module
        all_lines = lane_detector.get_lines(frame)
        avg_lines = lane_detector.get_average_lines(all_lines)
        if avg_lines is not None:
            avg_lines = [lane_detector.get_line_coordinates_from_parameters(
                frame, line) for line in avg_lines]
        if avg_lines is not None:
            for line in avg_lines:
                if line is not None:
                    obstacles.append({'points': [
                                     (line[0], line[1]), (line[2], line[3])],
                                     'distances': None, 'object_id': 4})

        # Use Traffic Sign module
        signs = traffic_sign_detector.detect_signs(frame)
        if signs is not None:
            for sign in signs:
                distances = path_finding.point_to_distance(
                    (sign[0]+sign[2]/2, sign[1]))
                distance_x = distances[0]
                distance_y = traffic_sign_detector.get_distance()
                obstacles.append({'points': [], 'distances': [
                                 (distance_x, distance_y)], 'object_id': 5})

        path_finding.insert_objects(obstacles)
        path_finding.calculate_path((460, 120))
