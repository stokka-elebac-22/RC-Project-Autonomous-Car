'''Main'''
import cv2
import pygame as pg
from pygame.locals import QUIT  # pylint: disable=no-name-in-module
from pathfinding import PathFinding
from lib import update_display
try:
    from line_detection.parking_slot_detection import ParkingSlotDetector
    from line_detection.lane_detection import LaneDetector
    from stop_sign_detection.stop_sign_detector import StopSignDetector, SignSize
    from environment.src.display import DisplayEnvironment
    from environment.src.environment import Environment, ViewPointObject
    from environment.src.a_star import AStar
    from qr_code.qr_code import QRCode, QRSize
    from camera_handler.camera import Camera
except ImportError:
    from computer_vision.line_detection.parking_slot_detection import ParkingSlotDetector
    from computer_vision.line_detection.lane_detection import LaneDetector
    from computer_vision.stop_sign_detection.stop_sign_detector import StopSignDetector, SignSize
    from computer_vision.environment.src.display import DisplayEnvironment
    from computer_vision.environment.src.environment import Environment, ViewPointObject
    from computer_vision.environment.src.a_star import AStar
    from computer_vision.qr_code.qr_code import QRCode
    from computer_vision.camera_handler.camera import Camera

if __name__ == '__main__':

    LIVE = False

    IMG_PATH = 'tests/images/simulation/title_3.jpg'
    #IMG_PATH = 'tests/images/mappingqr/title_2.jpg'

    if LIVE:
        cam = Camera(camera_id=0)
        ret, frame = cam.read()
        if not ret:
            raise ValueError('NO CAM FRAME')
    else:
        frame = cv2.imread(IMG_PATH)

    # ----- QR CODE ----- #
    QR_SIZE: QRSize = {
        'px': 191,
        'mm': 79,
        'distance': 515,
    }

    # ----- CAMERA ----- #
    PIXEL_WIDTH = frame.shape[1]
    PIXEL_HEIGHT = frame.shape[0]
    MM_WIDTH = 200

    # ----- ENVIRONMENT ----- #
    BOARD_SIZE = (60, 115)
    ENV_SIZE = 30
    W_SIZE = 720

    # ----- DISPLAY ----- #
    WINDOW_SIZE = (W_SIZE * (BOARD_SIZE[1]/BOARD_SIZE[0]), W_SIZE)
    TILE_SIZE = WINDOW_SIZE[1]/BOARD_SIZE[0]

    # ----- PARKING SLOT DETECTOR ----- #
    # OLD BOOMER
    P_CANNY = [50, 100]
    P_HOUGH = [65, 70, 20]
    P_ITERATIONS = [1, 1]
    P_BLUR = 12
    P_FILTER_ATOL = [20, 20]
    P_CLUSTER_ATOL = 0

    # P_CANNY = [50, 100]
    # P_HOUGH = [65, 70, 20]
    # P_ITERATIONS = [1, 1]
    # P_BLUR = 12
    # P_FILTER_ATOL = [20, 20]
    # P_CLUSTER_ATOL = 0

    # ----- LANE DETECTOR ----- #
    L_CANNY = [50, 100]
    L_HOUGH = [80, 200, 5]
    L_BLUR = 5

    # ----- STOP SIGN DETECTOR ----- #
    SIGN_SIZE: SignSize = {
        'px': 61,
        'mm': 10,
        'distance': 200,
    }

    # ----- PATHFINDING ----- #
    TENSION = 0
    VELOCITY = 10

    # environment
    view_point_object: ViewPointObject = {
        'view_point': None,
        'object_id': 10,
    }

    env = Environment(BOARD_SIZE, (PIXEL_WIDTH, PIXEL_HEIGHT), ENV_SIZE, view_point_object)

    # pathfinding algorithm
    a_star = AStar(weight=2, penalty=2, hindrance_ids=[1, 30])

    # display
    display = DisplayEnvironment(WINDOW_SIZE, BOARD_SIZE)

    path_finding = PathFinding(
        env,
        a_star,
        TENSION,
        VELOCITY
    )

    parking_slot_detector = ParkingSlotDetector(
        canny=P_CANNY,
        hough=P_HOUGH,
        blur=P_BLUR,
        iterations=P_ITERATIONS,
    )

    lane_detector = LaneDetector(
        canny=L_CANNY,
        blur=L_BLUR,
        hough=L_HOUGH,
        width=MM_WIDTH
    )

    stop_sign_detector = StopSignDetector(size=SIGN_SIZE)

    qr_code = QRCode(QR_SIZE)

    RUN = True
    objects = []

    while RUN:
        # Add hindrances using mouse
        for event in pg.event.get():
            if event.type == QUIT:
                RUN = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                col = mouse_pos[0] // TILE_SIZE
                row = mouse_pos[1] // TILE_SIZE
                objects.append(((int(row), int(col))))

        for obj in objects:
            env.insert_by_index(obj, 1)

        if LIVE:
            ret, frame = cam.read()
            if not ret:
                raise ValueError("NO CAM FRAME")
        else:
            frame = cv2.imread(IMG_PATH)

        obstacles = []

        qr_data = qr_code.get_data(frame)
        if qr_data['ret']:
            distances = env.point_to_distance(
                (qr_data['points'][0][0][0]+
                 (qr_data['points'][0][1][0]-qr_data['points'][0][0][0])/2,
                 qr_data['points'][0][0][0]))
            qr_distance_x = qr_code.qr_geometries[0].get_qr_code_distance_x((PIXEL_WIDTH/2, PIXEL_HEIGHT/2))
            qr_distance_y = qr_data['distances'][0]
            obstacles.append({'values': [
                (qr_distance_x, qr_distance_y)],
                'distance': True, 'object_id': 20})

            # Use ParkingSlot Module
            qr_code_data = {
                'ret': qr_data['ret'],
                'points': qr_data['points']
            }

            line_dict = parking_slot_detector.get_parking_slot(frame, qr_code_data)
            if line_dict is not None:
                for lines in line_dict['all_lines']:
                    obstacles.append({'values': [
                        (lines[0], lines[1]), (lines[2], lines[3])],
                        'distance': False, 'object_id': 30})
                for lines in line_dict['slot_lines']:
                    obstacles.append({'values': [
                        (lines[0], lines[1]), (lines[2], lines[3])],
                        'distance': False, 'object_id': 30})

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

            # Use Stop Sign module
            # signs = stop_sign_detection.detect_signs(frame)
            # if signs is not None:
            #     for sign in signs:
            #         distances = path_finding.point_to_distance(
            #             (sign[0]+sign[2]/2, sign[1]))
            #         distance_x = distances[0]
            #         distance_y = stop_sign_detection.get_distance(sign)
            #         obstacles.append({'values': [
            #         (distance_x, distance_y)], 'distance': True, 'object_id': 40})

            path_finding.insert_objects(obstacles)
            # TODO: point for lane line, maybe can remove the get course functions no need? # pylint: disable=W0511
            # check_point = lane_detector.get_next_point(frame, avg_lines)
            # path = path_finding.calculate_path(check_point, True)

            # With distance from Parking using QR!!!
            # TODO: DOES NOT WORK WHY?? maybe bcus of calibration constants # pylint: disable=W0511
            QR_CODE_ID = 20
            CAR_ID = 10
            path_data = path_finding.calculate_path(CAR_ID, QR_CODE_ID)
            if path_data is None:
                print('There is not path data...')
                continue
            update_display(display, path_finding.get_environment(), path_data['path'])
            display.display()

            path_finding.reset()

            # CATMULL SPLINE
            if path_data is not None:
                c = path_data['curve']
                # DRAW CATMULL LINE
                line_color = (255, 0, 0)

                pg.display.flip()
                COUNT = 0
                LEN_C = len(c)
                while COUNT < LEN_C - 1:
                    pg.draw.line(display.display_window, line_color,
                                (c[COUNT][0]*TILE_SIZE, c[COUNT][1]*TILE_SIZE),
                                (c[COUNT+1][0]*TILE_SIZE, c[COUNT+1][1]*TILE_SIZE))
                    COUNT += 2
                # 2D TO 3D, need to put in function?
                # for i, value in enumerate(c):
                #     if i % 30 == 0:
                #         distance_x = (value[0]-math.ceil(path_finding.env.size[1]/2)) \
                #                         *path_finding.env.real_size
                #         distance_y = (path_finding.env.size[0] -
                #                       (value[1]+1))*path_finding.env.real_size
                #         point = path_finding.distance_to_point((distance_x, distance_y))
                #         frame = cv2.circle(frame, point, 3, (255, 0, 0), -1)
    cv2.imshow('frame', frame)
    cv2.waitKey(0)
