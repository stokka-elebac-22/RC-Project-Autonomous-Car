'''
The main file for the driving logic.
This file should only contain short code
'''
import sys
import os
from typing import Tuple, List
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
        (config['environment']['sizey'], config['environment']['sizex']), PIXEL_WIDTH, PIXEL_HEIGHT,
        CAM_WIDTH, CAM_HEIGHT, center, display=display, env_size=20)

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
            # if ret -> replace the actions list

            # The environment objects is a list of tuples with
            # an distance (x and y) and the object id
            env_objects: List[Tuple[Tuple[int, int], int]] = []

            ### QR Code ###
            qr_data = qr_code.get_data(frame)
            if qr_data['ret']:
                qr_id = objects.get_data('QR').id
                distances = path_finding.point_to_distance(
                    (qr_data['points'][0][3][0]+qr_data['points'][0][2][0]/2,
                    qr_data['points'][0][0][0]))
                qr_distance_x = distances[0]
                qr_distance_y = qr_data['distances'][0]
                env_objects.append(qr_distance_x, qr_distance_y, qr_id)

            ### Line detection ###

            ### Traffic Sign Detection ###
            output_signs = traffic_sign_detection.detect_signs(frame)
            sign_id = objects.get_data('Stop').id
            for sign in output_signs:
                output_signs_distance = traffic_sign_detection.get_distance(sign)
                env_objects.append(output_signs_distance, sign_id)
            # traffic_sign_detection.show_signs(frame, output_signs)

            ### Lane Detection ###
                avg_lines = lane_detector.get_lane_line(frame)
            # lane_detector.show_lines(frame, avg_lines)
            next_point = lane_detector.get_next_point(frame, avg_lines)

            ### Parking Slot Detection ###
            parking_lines = parking_slot_detector.detect_parking_lines(frame, data)
            parking_lines.append(
                parking_slot_detector.get_closing_line_of_two_lines(parking_lines))
            # parking_slot_detector.show_lines(frame, parking_lines)

            # ---------- UPDATE ENVIRONMENT ---------- #
            # Insert objects into the environment
            for obj in env_objects:
                env.insert(env_objects[1], env_objects[0])

        # ---------- ACTION ---------- #
        match STATUS.active:
            case 'move':
                ret, current_action = action.next()
                if ret:
                    action.move(current_action)
                else:
                    # If there is no actions left -> do nothing
                    action.move(1, 0, 0)
