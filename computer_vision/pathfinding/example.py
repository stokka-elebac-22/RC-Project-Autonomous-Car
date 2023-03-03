'''Main'''
import math
import cv2
import pygame as pg
from pygame.locals import QUIT  # pylint: disable=no-name-in-module
from lib import PathFinding
from spline import catmull_rom_chain
from helping_functions import get_abs_velo, get_angle, get_angle_diff
from matplotlib import pyplot as plt
try:
    from line_detection.parking_slot_detection import ParkingSlotDetector
    from line_detection.lane_detection import LaneDetector
    from traffic_sign_detection.main import TrafficSignDetector
    from environment.src.display import DisplayEnvironment
    from qr_code.qr_code import QRCode
except ImportError:
    from computer_vision.line_detection.parking_slot_detection import ParkingSlotDetector
    from computer_vision.line_detection.lane_detection import LaneDetector
    from computer_vision.traffic_sign_detection.main import TrafficSignDetector
    from computer_vision.environment.src.display import DisplayEnvironment
    from computer_vision.qr_code.qr_code import QRCode

if __name__ == '__main__':

    CAM_WIDTH = 1000
    CAM_HEIGHT = 600

    BOARD_SIZE = (70, 115)
    ENV_SIZE = 20
    W_SIZE = 720

    img = cv2.imread(
        'tests/images/parking_slot_detection_2/frame_5_test.jpg')
    window_size = (W_SIZE * (BOARD_SIZE[1]/BOARD_SIZE[0]), W_SIZE)
    display = DisplayEnvironment(window_size, BOARD_SIZE)
    PIXEL_WIDTH = img.shape[1]
    PIXEL_HEIGHT = img.shape[0]
    path_finding = PathFinding(
        BOARD_SIZE, PIXEL_WIDTH, PIXEL_HEIGHT,
        CAM_WIDTH, CAM_HEIGHT, display=display, env_size=ENV_SIZE)
    parking_slot_detector = ParkingSlotDetector(
        canny=[50, 100],
        hough=[200, 50],
        blur=5,
        iterations=[1, 1],
        filter_atol=[20, 20],
        cluster_atol=5)
    lane_detector = LaneDetector()
    sign_size = {
        'px': 10,
        'mm': 61,
        'distance': 200
    }
    # qr_size = {
    #     'px': 10,
    #     'mm': 61,
    #     'distance': 200
    # }

    SIZE = {
        'px': 136,
        'mm': 79,
        'distance': 745
    }
    traffic_sign_detection = TrafficSignDetector(size=sign_size)
    qr_code = QRCode(SIZE)

    TILE_SIZE = display.window_size[1]/path_finding.size[0]

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
                path_finding.env.insert_by_index((int(row), int(col)), '1')

        # Should change this to camera frame later
        frame = cv2.imread(
        'tests/images/parking_slot_detection_2/frame_5_test.jpg')
        obstacles = []

        qr_data = qr_code.get_data(frame)
        if qr_data['ret']:
            distances = path_finding.point_to_distance(
                (qr_data['points'][0][3][0]+qr_data['points'][0][2][0]/2,
                 qr_data['points'][0][0][0]))
            qr_distance_x = distances[0]
            qr_distance_y = qr_data['distances'][0]
            # obstacles.append({'values': [
            #     (qr_distance_x, qr_distance_y)],
            #     'distance': True, 'object_id': 20})

        # Use ParkingSlot Module
        qr_code_data = {
            'ret': qr_data['ret'],
            'points': qr_data['points']
        }

        # TODO: TAKE THIS BACK
        # parking_slot_coords = parking_slot_detector.get_parking_slot(frame, qr_data)

        # if parking_slot_coords is not None:
        #     closing_line = parking_slot_detector.get_closing_line_of_two_lines(parking_slot_coords)
        #     if len(closing_line) == 4:
        #         parking_slot_coords.append(closing_line)
        #     for lines in parking_slot_coords:
        #         obstacles.append({'values': [
        #                          (lines[0], lines[1]), (lines[2], lines[3])],
        #             'distance': False, 'object_id': 30})
        # parking_lines, parking_lines_coords = parking_slot_detector.get_parking_lines(frame)

        parking_lines_coords = [[64, 642, 207, 556],
[427, 648, 460, 561],
[795, 648, 718, 565],
[1143, 650, 967, 565]]
        if parking_lines_coords is not None:
            for lines in parking_lines_coords:
                obstacles.append({'values': [
                                 (lines[0], lines[1]), (lines[2], lines[3])],
                    'distance': False, 'object_id': 30})
                
        
        # parking_slot_coords = parking_slot_detector.get_parking_slot(frame, qr_data)

        # if parking_slot_coords is not None:
        #     closing_line = parking_slot_detector.get_closing_line_of_two_lines(parking_slot_coords)
        #     if len(closing_line) == 4:
        #         parking_slot_coords.append(closing_line)
        #     for lines in parking_slot_coords:
        #         obstacles.append({'values': [
        #                          (lines[0], lines[1]), (lines[2], lines[3])],
        #             'distance': False, 'object_id': 30})


        # Use lane Module
        # avg_lines = lane_detector.get_lane_line(frame)
        # if avg_lines is not None:
        #     for line in avg_lines:
        #         if line is not None:
        #             obstacles.append({'values': [
        #                              (line[0], line[1]), (line[2], line[3])],
        #                 'distance': False, 'object_id': 31})

        #     center_diff = lane_detector.get_diff_from_center_info(
        #         frame, avg_lines)

        #TODO: fix this to use warping instead of just forwarding
        # CENTER_DIFF_X = 0
        # CENTER_DIFF_Y = 0
        # if center_diff is not None:
        #     CENTER_DIFF_X = center_diff
        #     DESIRED_DISTANCE_FORWARD = 100
        # Use Traffic Sign module
        # signs = traffic_sign_detection.detect_signs(frame)
        # if signs is not None:
        #     for sign in signs:
        #         distances = path_finding.point_to_distance(
        #             (sign[0]+sign[2]/2, sign[1]))
        #         distance_x = distances[0]
        #         distance_y = traffic_sign_detection.get_distance(sign)
        #         obstacles.append({'values': [
        #                          (distance_x, distance_y)], 'distance': True, 'object_id': 40})

        path_finding.insert_objects(obstacles)
        # TODO: Remove later since Test point # pylint: disable=W0511
        path = path_finding.calculate_path((460, 120), False)
        path_finding.update_display(path)
        path_finding.display.display()


        # CATMULL SPLINE
        TENSION = 0.

        if path:
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

            # DRAW CATMULL LINE
            line_color = (255, 0, 0)

            pg.display.flip()
            COUNT = 0
            LEN_C = len(c)
            while COUNT < LEN_C:
                pg.draw.line(path_finding.display.display_window, line_color,
                            (c[COUNT][0]*TILE_SIZE, c[COUNT][1]*TILE_SIZE),
                            (c[COUNT+1][0]*TILE_SIZE, c[COUNT+1][1]*TILE_SIZE))
                COUNT += 2

        # RUN = True
        # TODO: point for lane line, maybe can remove the get course functions no need? # pylint: disable=W0511
        # path_finding.calculate_path((CENTER_DIFF_X, DESIRED_DISTANCE_FORWARD), True)

        # With distance from Parking using QR!!!
        # TODO: DOES NOT WORK WHY?? maybe bcus of calibration constants # pylint: disable=W0511
        # path_finding.calculate_path((qr_distance_x, qr_distance_y), True)

        # TODO: add catmull rom spline based on points given by path # pylint: disable=W0511
        # USE PATH variable!!!


            # ANGLE DIFF calculation
            x_values = [i[0] for i in c]
            y_values = [i[1] for i in c]
            vx_values = [i[0] for i in v]
            vy_values = [i[1] for i in v]

    # CURRENT_ANG = 0
    # angle_diff = []
    # angle_diff_x = []
    # for i, next_ang in enumerate(angles):
    #     angle_diff_x.append(i)
    #     first_diff = math.dist([CURRENT_ANG], [next_ang])
    #     second_diff = 360-abs(first_diff)
    #     minimum_diff = min(abs(first_diff), second_diff)
    #     if CURRENT_ANG > 0 and next_ang < 0:
    #         minimum_diff = minimum_diff*-1

    #     angle_diff.append(minimum_diff)
    #     CURRENT_ANG = next_ang

            angle_diff = get_angle_diff(angles)
            angle_diff_x = [i for i in range(len(angle_diff))]

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
