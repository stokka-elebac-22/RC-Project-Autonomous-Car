'''main_headless.py: DATBAC23 Car system main.'''
import time
from typing import List
from collections import deque
from defines import States, MessageId
from socket_handling.abstract_server import NetworkSettings
from socket_handling.multi_socket_server import MultiSocketServer
from camera_handler.camera_headless import CameraHandler
from camera_handler.camera_sock_server import CamSocketStream
from line_detection.lane_detection import LaneDetector
from line_detection.parking_slot_detection import ParkingSlotDetector
from traffic_sign_detection.traffic_sign_detector import TrafficSignDetector
from car_communication.abstract_communication import AbstractCommunication
from car_communication.can_bus_communication import CanBusCommunication
from car_communication.car_serial_communication import CarSerialCommunication
from car_communication.car_stepper_communication import CarStepperCommunication
from environment.src.environment import Environment
from environment.src.a_star import AStar
from pathfinding.pathfinding import PathFinding
from qr_code.qr_code import QRCode, QRSize

class Headless():  # pylint: disable=R0903
    '''Class handling headless running'''
    # pylint: disable=R0902
    def __init__(self, conf: dict): # pylint: disable=R0912, R0914, R0915
        self.state = States.WAITING  # Start in "idle" state
        self.car_comm: AbstractCommunication
        # pylint: disable=R0903
        if conf["car_comm_interface"] == "serial":
            self.car_comm = CarSerialCommunication(conf["serial"])
        elif conf["car_comm_interface"] == "can":
            self.car_comm = CanBusCommunication(conf["can"])
        elif conf["car_comm_interface"] == "stepper":
            self.car_comm = CarStepperCommunication(conf["stepper"])

        # Network config for main connection + camera(s)
        self.net_main = NetworkSettings(conf["network"]["host"], conf["network"]["port"])
        self.net_cam0 = NetworkSettings(conf["network"]["host"], conf["network"]["port_cam0"])
        self.net_cam1 = NetworkSettings(conf["network"]["host"], conf["network"]["port_cam1"])

        # Start main socket server for connections
        self.socket_server = MultiSocketServer(self.net_main)
        self.socket_server.start()

        self.cam0_stream = CamSocketStream(self.net_cam0)
        if conf["network"]["stream_en_cam0"] is True:
            self.cam0_stream.start()

        self.cam1_stream = CamSocketStream(self.net_cam1)
        if conf["network"]["stream_en_cam1"] is True:
            self.cam1_stream.start()

        self.cam0_handler = CameraHandler(conf["camera0"]["id"])


        # ---------- INIT ENVIRONMENT ---------- #
        env_size = conf['environment']['size']
        self.env= Environment(env_size, conf['environment']['real_size'], {'object_id': 10})

        # ---------- INIT TRAFFIC SIGN DETECTOR ---------- #
        traffic_size: QRSize = {
            'px': conf['sign_size']['px'],
            'mm': conf['sign_size']['mm'],
            'distance': conf['sign_size']['distance'],
        }
        min_size_traffic = conf['traffic_sign']['min_size']
        self.stop_sign_detector = TrafficSignDetector('cascade.xml',
                                                      traffic_size,
                                                      min_size_traffic)

        # ---------- INIT PARKING SLOT DETECTOR ---------- #
        parking_slot_detector = ParkingSlotDetector(
            canny=conf['parking_slot_detector']['canny'],
            hough=conf['parking_slot_detector']['hough'],
            blur=conf['parking_slot_detector']['blur'],
            iterations=conf['parking_slot_detector']['iterations'],
            filter_atol=conf['parking_slot_detector']['canny'],
        )

        # ---------- INIT LANE DETECTOR ---------- #
        lane_detector = LaneDetector(
            canny=conf['lane_detector']['canny'],
            blur=conf['lane_detector']['blur'],
            hough=conf['lane_detector']['hough'],
            width=conf['lane_detector']['width']
        )

        # ---------- INIT PATHFINDING ALGORITHM ---------- #
        a_star = AStar(conf['a_star']['weight'], conf['a_star']['penalty'])

        # ---------- INIT PATHFINDING ---------- #
        # finding the center of the camera

        _, frame = self.cam0_handler.get_cv_frame()
        if frame is None:
            raise ConnectionError
        frame_width, frame_height, _ = frame.shape
        path_finding: PathFinding = PathFinding(
            pixel_size=(frame_width, frame_height),
            environment=self.env,
            pathfinding_algorithm=a_star,
            tension=conf['spline']['tension'],
            velocity=conf['spline']['velocity']
        )

        # ---------- INIT QR CODE ---------- #
        qr_size: QRSize = {
            'px': conf['qr_code_size']['px'],
            'mm': conf['qr_code_size']['mm'],
            'distance': conf['qr_code_size']['distance'],
        }
        self.qr_code = QRCode(qr_size)

        ### Object IDS ###
        qr_code_id = conf['object_id']['QR']
        car_id = conf['object_id']['car']
        end_point_id = conf['object_id']['end_point']
        lane_line_id = conf['object_id']['lane_line']
        parking_line_id = conf['object_id']['parking_line']


        ### ACTION ###
        actions_resetted = False
        self.previous = {
            'angle': None,
            'speed': None,
            'time': time.time(),
        }

        # base = 100
        self.previous_time = time.time()
        while True: # pylint: disable=R1702
            # Check and handle incoming data
            for data in self.socket_server:
                if MessageId(data[0]) is MessageId.CMD_SET_STATE:
                    self.state = data[1]
                    print("State changed to: ")
                    print(States(data[1]).name)

            # Take new picture, handle socket transfers
            ret, frame0 = self.cam0_handler.get_cv_frame()
            if ret is True:
                self.cam0_stream.send_to_all(frame0)
                self.cam1_stream.send_to_all(frame0)

            if self.state is States.WAITING:  # Prints detected data (testing)

                current_stop_sign = self.stop_sign_detector.detect_signs(frame)
                if len(current_stop_sign) > 0:
                    print(current_stop_sign)

                # ---------- QR-Code ---------- #
                current_qr_data = self.qr_code.get_data(frame)
                output_data = 'Data: \n'
                # print(current_qr_data)
                if current_qr_data['ret']:
                    for i in range(len(current_qr_data['distances'])):
                        output_data += \
                            f"QR-Code {str(i)} \n \
                                Distance: {round(current_qr_data['distances'][i])} \n \
                                Angle: {current_qr_data['angles'][i]} \n"
                        output_data += 'Data: ' + current_qr_data['info'][i] + '\n'
                    if current_qr_data['distances'] is not None and \
                            len(current_qr_data['distances']) > 0:
                        print(output_data)

            elif self.state is States.PARKING:
                # ---------- Parking Slot ---------- #
                objects: List[path_finding.Objects] = []

                # # ---------- GET CAMERA INFORMATION---------- #
                # frame = self.cam0_handler.get_cv_frame()
                # if frame is None:
                #     continue

                ## QR Code ###
                qr_data = self.qr_code.get_data(frame)
                if not qr_data['ret']:
                    continue

                # add qr code to the objects list
                qr_code_distances = []
                for geo in self.qr_code.qr_geometries:
                    qr_code_distances.append((
                        geo.get_qr_code_distance_x(),
                        geo.get_distance()))

                path_finding_object: path_finding.Objects = {
                    'values': [qr_code_distances],
                    'distance': True,
                    'object_id': qr_code_id
                }
                objects.append(path_finding_object)

                line_dict = parking_slot_detector.get_parking_slot(frame, qr_data)
                if line_dict is not None:
                    for lines in line_dict['all_lines']:
                        objects.append({'values': [
                            (lines[0], lines[1]), (lines[2], lines[3])],
                            'distance': False, 'object_id': 30})
                    for lines in line_dict['slot_lines']:
                        objects.append({'values': [
                            (lines[0], lines[1]), (lines[2], lines[3])],
                            'distance': False, 'object_id': parking_line_id})

                # ---------- UPDATE ENVIRONMENT ---------- #
                path_finding.reset()
                path_finding.insert_objects(objects)

                # ---------- PATH ---------- #
                if len(qr_code_distances) > 0:
                # ---------- SPLINES ---------- #
                    path_data = path_finding.calculate_path(car_id, qr_code_id)

                # ---------- ACTIONS ---------- #
                    if path_data is not None:
                        angles = path_data['angles']
                        times = path_data['times']
                        self.actions: deque = deque()
                        for angle, action_time in zip(angles, times):
                            self.actions.append({
                                'speed': conf['spline']['velocity'],
                                'angle': angle,
                                'time': action_time,
                            })
                        actions_resetted = True

            elif self.state is States.DRIVING:
                # ---------- Lane Detection ---------- #
                objects: List[path_finding.Objects] = []
                avg_lines = lane_detector.get_lane_line(frame)
                if avg_lines is not None:
                    for line in avg_lines:
                        if line is not None:
                            objects.append({'values': [
                                            (line[0], line[1]), (line[2], line[3])],
                                'distance': False, 'object_id': lane_line_id})
                    check_point = lane_detector.get_next_point(frame, avg_lines)
                    if check_point is not None:
                        objects.append({'values': [check_point],
                                    'distance': False, 'object_id': lane_line_id})

                        path_data = path_finding.calculate_path(check_point, False)

                        # ---------- UPDATE ENVIRONMENT ---------- #
                        path_finding.reset()
                        path_finding.insert_objects(objects)

                        # ---------- PATH ---------- #
                        path_data = path_finding.calculate_path(car_id, end_point_id)

                        # ---------- ACTIONS ---------- #
                        if path_data is not None:
                            angles = path_data['angles']
                            times = path_data['times']
                            self.actions: deque = deque()
                            for angle, action_time in zip(angles, times):
                                self.actions.append({
                                    'speed': conf['spline']['velocity'],
                                    'angle': angle,
                                    'time': action_time,
                                })
                            actions_resetted = True

            elif self.state is States.STOPPING:
                # ---------- Traffic Sign Detection ---------- #
                current_stop_signs = self.stop_sign_detector.detect_signs(frame)
                no_sign = True
                if len(current_stop_signs) > 0:
                    for sign in current_stop_signs:
                        distance = self.stop_sign_detector.get_distance(sign)
                        no_sign = False
                        if distance <= conf['traffic_sign_detector']['distance']:
                            self.actions = deque()
                            self.actions.append({
                                                'speed': 0,
                                                'angle': 0,
                                                'time': 0,
                            })
                if no_sign:
                    self.actions.append({
                            'speed': conf['base_speed'],
                            'angle': 0,
                            'time': 0,
                    })

            time_now = self.previous_time - time.time()

            if self.cur_action is None or \
                (self.cur_action is not None and time_now > self.cur_action['time'])\
                    or actions_resetted:
                new_action = self.actions.popleft()
                if new_action is not None: 
                    if self.previous['speed'] != new_action['speed'] and \
                        self.previous['angle'] != new_action('angle'):
                        self.car_comm.drive_direction(new_action['speed'], new_action('angle'))
                        self.previous['speed'] = new_action['speed']
                        self.previous['angle'] = new_action('angle')
                        self.previous['time'] = time.time()
                else:
                    if self.state != States.DRIVING:
                        self.car_comm.drive_direction(0, 0)
                    else:
                        self.car_comm.drive_direction(0, self.conf['base_speed'])
