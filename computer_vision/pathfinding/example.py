'''Main'''
import math
import cv2
import pygame as pg
from pygame.locals import QUIT  # pylint: disable=no-name-in-module
from pathfinding import PathFinding
from spline import catmull_rom_chain
from lib import get_abs_velo, get_angle, update_display
from matplotlib import pyplot as plt

try:
    from line_detection.parking_slot_detection import ParkingSlotDetector
    from line_detection.lane_detection import LaneDetector
    from traffic_sign_detection.traffic_sign_detector import TrafficSignDetector, SignSize
    from environment.src.display import DisplayEnvironment
    from environment.src.environment import Environment, ViewPointObject
    from environment.src.a_star import AStar
    from qr_code.qr_code import QRCode, QRSize
except ImportError:
    from computer_vision.line_detection.parking_slot_detection import ParkingSlotDetector
    from computer_vision.line_detection.lane_detection import LaneDetector
    from computer_vision.traffic_sign_detection.traffic_sign_detector import TrafficSignDetector, SignSize
    from computer_vision.environment.src.display import DisplayEnvironment
    from computer_vision.environment.src.environment import Environment, ViewPointObject
    from computer_vision.environment.src.a_star import AStar
    from computer_vision.qr_code.qr_code import QRCode

if __name__ == '__main__':

    # ----- QR CODE ----- #
    QR_SIZE: QRSize = {
        'px': 76,
        'mm': 52,
        'distance': 500,
    }

    # ----- CAMERA ----- #
    PIXEL_WIDTH = 500
    PIXEL_HEIGHT = 300
    CAM_WIDTH = 800
    CAM_HEIGHT = 500

    # ----- ENVIRONMENT ----- #
    BOARD_SIZE = (60, 115)
    ENV_SIZE = 20
    W_SIZE = 720

    # ----- PARKING SLOT DETECTOR ----- #
    HOUGH = [200, 5]
    ITERATIONS = [5, 2]

    # ----- TRAFFIC SIGN DETECTOR ----- #
    TRAFFIC_SIGN_SIZE_MM = 61
    TRAFFIC_SIGN_SIZE_PX = 10
    TRAFFIC_SIGN_DISTANCE = 200
    sign_size: SignSize = {
        'px': 61,
        'mm': 10,
        'distance': 200,
    }

    # reading image
    IMG_PATH = 'computer_vision/line_detection/assets/parking/10.png'
    img = cv2.imread(IMG_PATH)

    # find center and window size
    CENTER = (img.shape[1], img.shape[0])
    WINDOW_SIZE = (W_SIZE * (BOARD_SIZE[1]/BOARD_SIZE[0]), W_SIZE)

    # calculate tile size
    TILE_SIZE = WINDOW_SIZE[1]/BOARD_SIZE[0]

    # environment
    view_point_object: ViewPointObject = {
        'view_point': None,
        'object_id': 10,
    }
    env = Environment(BOARD_SIZE, ENV_SIZE, view_point_object)

    # pathfinding algorithm
    a_star = AStar()

    # display
    display = DisplayEnvironment(WINDOW_SIZE, BOARD_SIZE)

    path_finding = PathFinding(
        [PIXEL_WIDTH, PIXEL_HEIGHT],
        [CAM_WIDTH, CAM_HEIGHT],
        CENTER,
        env,
        a_star)

    parking_slot_detector = ParkingSlotDetector(
        hough=HOUGH,
        iterations=ITERATIONS)
    lane_detector = LaneDetector()
    traffic_sign_detector = TrafficSignDetector(size=sign_size)

    qr_code = QRCode(QR_SIZE)

    RUN = True
    while RUN:
        # Add hindrances using mouse
        for event in pg.event.get():
            if event.type == QUIT:
                RUN = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                col = mouse_pos[0] // TILE_SIZE
                row = mouse_pos[1] // TILE_SIZE
                path_finding.environment.insert_by_index((int(row), int(col)), '1')

        # Should change this to camera frame later
        frame = cv2.imread(IMG_PATH)
        obstacles = []

        qr_data = qr_code.get_data(frame)
        if qr_data['ret']:
            distances = path_finding.point_to_distance(
                (qr_data['points'][0][3][0]+qr_data['points'][0][2][0]/2,
                 qr_data['points'][0][0][0]))
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

        parking_lines = parking_slot_detector.get_parking_slot(
            frame, qr_code_data)

        parking_lines.append(
            parking_slot_detector.get_closing_line_of_two_lines(parking_lines))

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

            center_diff = lane_detector.get_diff_from_center_info(
                frame, avg_lines)

        #TODO: fix this to use warping instead of just forwarding
            CENTER_DIFF_X = 0
            CENTER_DIFF_Y = 0
            if center_diff is not None:
                CENTER_DIFF_X = center_diff
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
                                 (distance_x, distance_y)], 'distance': True, 'object_id': 5})

        path_finding.insert_objects(obstacles)
        # TODO: Remove later since Test point # pylint: disable=W0511
        path = path_finding.calculate_path((460, 120), False)

        update_display(display, env, path)
        display.display()

        TENSION = 0.

        new_path = [(value[1], value[0])
                    for i, value in enumerate(path) if i % 3 == 0]
        temp_path = [(path[0][1], path[0][0])]
        temp_path = temp_path + new_path
        for _ in range(2):
            temp_path.append((path[len(path) - 1][1], path[len(path) - 1][0]))

        temp_path.reverse()
        c, v = catmull_rom_chain(temp_path, TENSION)
        # x_values, y_values = zip(*c)
        abs_velos = []
        angles = []
        for value in v:
            abs_velos.append(get_abs_velo(value))
            angles.append(get_angle(value))

        # CHECK DIFF WITH NEXT ONE TO SEE IF TURN RIGHT OR LEFT AND AMOUNT OF TURN
        # diff = velocities[i] - velocities[i+1]
        # if positive: rotate clockwise
        # else rotate counter clockwise

        line_color = (255, 0, 0)

        pg.display.flip()
        COUNT = 0
        LEN_C = len(c)
        while COUNT < LEN_C:
            pg.draw.line(display.display_window, line_color,
                         (c[COUNT][0]*TILE_SIZE, c[COUNT][1]*TILE_SIZE),
                         (c[COUNT+1][0]*TILE_SIZE, c[COUNT+1][1]*TILE_SIZE))
            COUNT += 2

        # RUN = True
        # TODO: point for lane line, maybe can remove the get course functions no need? # pylint: disable=W0511
        # path_finding.calculate_path((CENTER_DIFF_X, CENTER_DIFF_Y), True)

        # With distance from Parking using QR!!!
        # TODO: DOES NOT WORK WHY?? maybe bcus of calibration constants # pylint: disable=W0511
        # path_finding.calculate_path((qr_distance_x, DESIRED_DISTANCE_FORWARD), True)

        # TODO: add catmull rom spline based on points given by path # pylint: disable=W0511
        # USE PATH variable!!!


    # ANGLE DIFF calculation
    x_values = [i[0] for i in c]
    y_values = [i[1] for i in c]
    vx_values = [i[0] for i in v]
    vy_values = [i[1] for i in v]

    CURRENT_ANG = 0
    angle_diff = []
    angle_diff_x = []
    for i, next_ang in enumerate(angles):
        angle_diff_x.append(i)
        first_diff = math.dist([CURRENT_ANG], [next_ang])
        second_diff = 360-abs(first_diff)
        minimum_diff = min(abs(first_diff), second_diff)
        if CURRENT_ANG > 0 and next_ang < 0:
            minimum_diff = minimum_diff*-1

        angle_diff.append(minimum_diff)
        CURRENT_ANG = next_ang

    fig, axs = plt.subplots(1, 3)
    fig.suptitle('Horizontally stacked subplots')
    axs[0].plot(x_values, y_values)
    axs[0].quiver(x_values, y_values, vx_values, vy_values, linewidths=1)
    axs[1].plot(angle_diff_x, angles)
    axs[2].plot(angle_diff_x, angle_diff)
    plt.show()

    # 2D TO 3D, need to put in function?
    for i, value in enumerate(c):
        if i % 30 == 0:
            distance_x = (value[0]-math.ceil(path_finding.env.size[1]/2)) \
                            *path_finding.env.real_size
            distance_y = (path_finding.env.size[0] - (value[1]+1))*path_finding.env.real_size
            point = path_finding.distance_to_point((distance_x, distance_y))
            frame = cv2.circle(frame, point, 3, (255, 0, 0), -1)
    cv2.imshow('frame', frame)
    cv2.waitKey(0)
