'''
The main file for the driving logic.
This file should only contain short code
'''
import sys
import os
import math
# from typing import Tuple, List
import yaml
from lib import Status, Action

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# pylint: disable=C0413
from computer_vision.qr_code.qr_code import QRCode
from computer_vision.environment.src.environment import Environment
from computer_vision.environment.src.lib import Objects
# from computer_vision.camera_handler.camera import Camera
from computer_vision.camera_handler.camera_handler import CameraHandler
from computer_vision.camera_handler.camera import Camera
from computer_vision.traffic_sign_detection.main import TrafficSignDetector
from computer_vision.line_detection.parking_slot_detection import ParkingSlotDetector
from computer_vision.line_detection.lane_detection import LaneDetector
from computer_vision.pathfinding.lib import PathFinding
from computer_vision.pathfinding.helping_functions import get_abs_velo, get_angle, get_angle_diff
from computer_vision.pathfinding.spline import catmull_rom_chain

# ---------- CONSTANTS ---------- #

# ---------- MAIN ---------- #
if __name__ == '__main__':
    with open('driving/config.yaml', 'r', encoding='utf8') as file:
        config = yaml.safe_load(file)

    # ---------- INIT ---------- #
    ### init camera ###
    ### init qr code ###
    qr_size = {
        'px': config['qr_code_size']['px'],
        'mm': config['qr_code_size']['mm'],
        'distance': config['qr_code_size']['distance']
    }
    qr_code = QRCode(qr_size)

    ### init traffic sign detector ###
    sign_size = {
        'px': config['sign_size']['px'],
        'mm': config['sign_size']['mm'],
        'distance': config['sign_size']['distance']
    }
    traffic_sign_detection = TrafficSignDetector(size=sign_size)

    ### init lane detector ###

    lane_detector = LaneDetector(
        config['lane_detector']['canny'],
        config['lane_detector']['blur'],
        config['lane_detector']['hough'],
        config['lane_detector']['width'])

    ### init parking slot detector ###
    parking_slot_detector = ParkingSlotDetector(
        hough=config['parking_slot_detector']['hough'],
        iterations=config['parking_slot_detector']['iterations'])

    ### init environment ###
    SIZE = (config['environment']['sizex'], config['environment']['sizey'])
    WINDOW_WIDTH = config['gui']['window_width']
    WINDOW_SIZE = (WINDOW_WIDTH* (SIZE[1]/SIZE[0]), WINDOW_WIDTH)
    env= Environment(SIZE, 1, {'object_id': 10})
    objects = Objects()

    ### init pathfinding ###
    path_finding = PathFinding(
        (config['environment']['sizey'], config['environment']['sizex']),
        config['camera']['px_width'], config['camera']['px_height'],
        config['camera']['mm_width'], config['camera']['mm_width'], None, env_size=20)

    camera_handler = CameraHandler()
    camera_handler.refresh_camera_list()
    available_cameras = camera_handler.get_camera_list()
    camera = Camera(available_cameras[0]['id'])

    # assuming the first camera is the correct one
    CAMERA = None
    if len(available_cameras) != 0:
        camera_id = available_cameras[0].get('id')
        # CAMERA = Camera(camera_id)

    STATUS: Status = Status()
    action = Action()

    # ---------- LOOP ---------- #
    while True:
        # ---------- GET CAMERA INFORMATION---------- #
        ### Get frame ###
        ret, frame = camera.read()
        # if ret is false, then no frame is available and then should
        # use the stored actions
        if ret:

            env_objects = []
            # if ret -> replace the actions list

            # The environment objects is a list of tuples with
            # an distance (x and y) and the object id
            #env_objects: List[Tuple[Tuple[int, int], int]] = []

            ### QR Code ###
            qr_data = qr_code.get_data(frame)
            if qr_data['ret']:
                qr_id = objects.get_data('QR').id
                distances = path_finding.point_to_distance(
                    (qr_data['points'][0][3][0]+qr_data['points'][0][2][0]/2,
                    qr_data['points'][0][0][0]))
                qr_distance_x = distances[0]
                qr_distance_y = qr_data['distances'][0]
                #env_objects.append(qr_distance_x, qr_distance_y, qr_id)

            ### Traffic Sign Detection ###
            signs = traffic_sign_detection.detect_signs(frame)
            if signs is not None:
                for sign in signs:
                    distances = path_finding.point_to_distance(
                        (sign[0]+sign[2]/2, sign[1]))
                    distance_x = distances[0]
                    distance_y = traffic_sign_detection.get_distance(sign)
                    env_objects.append({'values': [
                                    (distance_x, distance_y)], 'distance': True, 'object_id': 40})

            ### Lane Detection ###

            lane_lines = lane_detector.get_lane_line(frame)
            if lane_lines is not None:
                for line in lane_lines:
                    if line is not None:
                        env_objects.append({'values': [
                                        (line[0], line[1]), (line[2], line[3])],
                            'distance': False, 'object_id': 31})

                # center_diff = lane_detector.get_diff_from_center_info(
                #     frame, lane_lines)
                next_point = lane_detector.get_next_point(frame, lane_lines)
                # TODO: endre 40 til noe annet.
                env_objects.append({'values': [
                                    next_point], 'distance': False, 'object_id': 40})

            # Use ParkingSlot Module
            qr_code_data = {
                'ret': qr_data['ret'],
                'points': qr_data['points']
            }
            parking_lines, parking_lines_coords = parking_slot_detector.get_parking_lines(frame)

            if parking_lines_coords is not None:
                for lines in parking_lines_coords:
                    env_objects.append({'values': [
                                    (lines[0], lines[1]), (lines[2], lines[3])],
                        'distance': False, 'object_id': 30})

            parking_slot_coords = parking_slot_detector.get_parking_slot(frame, qr_data)

            if parking_slot_coords is not None:
                closing_line = parking_slot_detector.get_closing_line_of_two_lines(
                    parking_slot_coords)
                if len(closing_line) == 4:
                    parking_slot_coords.append(closing_line)
                for lines in parking_slot_coords:
                    env_objects.append({'values': [
                                    (lines[0], lines[1]), (lines[2], lines[3])],
                        'distance': False, 'object_id': 30})

            # ---------- UPDATE ENVIRONMENT ---------- #
            # Insert objects into the environment
            path_finding.insert_objects(env_objects)
            # TODO: add qr or checkpoint as calculated path
            path = path_finding.calculate_path((460, 120), False)
            # LANE NEXT POINT
            # path = path_finding.calculate_path(point, False)
            # QR CODE
            # path = path_finding.calculate_path(
            # (qr_distance_x, config['lane_detector']['forward']), True)

            # ---------- CALCULATE VELOCITY AND ANGLE ---------- #
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

            angle_diff = get_angle_diff(angles)

        # ---------- ACTION ---------- #
        match STATUS.active:
            case 'move':
                ret, current_action = action.next()
                if ret:
                    action.move(current_action)
                else:
                    # If there is no actions left -> do nothing
                    action.move(1, 0, 0)
