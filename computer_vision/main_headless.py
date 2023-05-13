'''main_headless.py: DATBAC23 Car system main.'''
import time
from typing import List, TypedDict
from collections import deque
import cv2
from defines import States, MessageId
from joystick_handler.joystick_position import CurrentHeading
from socket_handling.abstract_server import NetworkSettings
from socket_handling.multi_socket_server import MultiSocketServer
from camera_handler.camera_headless import CameraHandler
from camera_handler.camera_sock_server import CamSocketStream
from car_communication.abstract_communication import AbstractCommunication
from car_communication.can_bus_communication import CanBusCommunication
from car_communication.car_serial_communication import CarSerialCommunication
from car_communication.car_stepper_communication import CarStepperCommunication
from environment.src.environment import Environment, ViewPointObject

from states.manual import ManualDriving
from states.waiting import WaitingState
from states.stopping import StopSignAction
from states.driving import LaningAction
from states.parking import ParkingAction
from states.stereo import StereoAction

ActionsDict = TypedDict('ActionsDict', {
    'speed': int,
    'angle': float,
    'time': float,
})


class Headless():  # pylint: disable=R0903
    '''Class handling headless running'''
    # pylint: disable=R0902
    # pylint: disable=R0915

    def __init__(self, conf: dict):  # pylint: disable=R0912
        self.state = States.WAITING  # Start in "idle" state
        self.conf = conf
        self.actions: List[ActionsDict] = deque()
        self.cur_action = None
        self.prev_action = {
            'angle': None,
            'speed': None,
            'time': time.time(),
        }
        path_data = None

        self.car_comm: AbstractCommunication
        # pylint: disable=R0903
        if conf["car_comm_interface"] == "serial":
            self.car_comm = CarSerialCommunication(conf["serial"])
        elif conf["car_comm_interface"] == "can":
            self.car_comm = CanBusCommunication(conf["can"])
        elif conf["car_comm_interface"] == "stepper":
            print("Selected stepper")
            self.car_comm = CarStepperCommunication(conf["step"])
        self.car_comm.start()
        # Network config for main connection + camera(s)
        self.net_main = NetworkSettings(
            conf["network"]["host"], conf["network"]["port"])
        self.net_cam0 = NetworkSettings(
            conf["network"]["host"], conf["network"]["port_cam0"])
        self.net_cam1 = NetworkSettings(
            conf["network"]["host"], conf["network"]["port_cam1"])

        # Start main socket server for connections
        self.socket_server = MultiSocketServer(self.net_main)
        self.socket_server.start()

        self.camera_missing_frame = 0
        self.joystick_position = CurrentHeading()

        self.cam0_stream = CamSocketStream(self.net_cam0)
        if conf["network"]["stream_en_cam0"] is True:
            print("Starting camera stream")
            self.cam0_stream.start()

        self.cam1_stream = CamSocketStream(self.net_cam1)
        if conf["network"]["stream_en_cam1"] is True:
            self.cam1_stream.start()

        # Get size from config
        size = {
            'px': conf["camera0"]["size"]["px"],
            'mm': conf["camera0"]["size"]["mm"],
            'distance': conf["camera0"]["size"]["distance"],
        }

        if conf["camera0"]["enabled"] is True:
            self.cam0_handler = CameraHandler(conf["camera0"]["id"])
        else:
            self.cam0_handler = None

        if conf["camera1"]["enabled"] is True:
            self.cam1_handler = CameraHandler(conf['camera1']['id'])
        else:
            self.cam1_handler = None

            # ----- CAMERA ----- #
        PIXEL_WIDTH, PIXEL_HEIGHT = conf["camera"]["camera_resolution"]["web"]
        # PIXEL_HEIGHT = conf['frame'][1]

        # ----- ENVIRONMENT ----- #
        BOARD_SIZE = (60, 115)
        ENV_SIZE = 30

        view_point_object: ViewPointObject = {
            'view_point': None,
            'object_id': 10,
        }

        env = Environment(BOARD_SIZE, (PIXEL_WIDTH, PIXEL_HEIGHT),
                          ENV_SIZE, view_point_object)


        self.waiting_state = WaitingState(size)
        self.stopping_state = StopSignAction('stop_sign_model.xml')
        self.driving_state = LaningAction(conf, env)
        self.parking_state = ParkingAction(conf, env)
        self.stereo_vision = StereoAction(conf)
        ret1 = False
        while True:
            # Check and handle incoming data
            for data in self.socket_server:
                print(data)
                if MessageId(data[0]) is MessageId.CMD_SET_STATE:
                    self.state = States(data[1])
                    print(f"State changed to: {self.state} - ")
                    print(States(data[1]).name)
                if MessageId(data[0]) is MessageId.CMD_JOYSTICK_DIRECTIONS:
                    self.joystick_position.set_heading_from_bytes(data)
                    # Handle joystick directions

            # Take new picture, handle socket transfers
            ret, frame0 = self.cam0_handler.get_cv_frame()
            if self.cam1_handler is not None:
                ret1, frame1 = self.cam1_handler.get_cv_frame()
            if ret is True:
                self.camera_missing_frame = 0
                self.cam0_stream.send_to_all(frame0)
            else:
                self.camera_missing_frame += 1
                print(
                    f"Could not get frame from camera: {self.cam0_handler.camera_id}!")
                if self.camera_missing_frame > 10:
                    print(
                        "Exceeded number of missing frames in a row. Stopping headless.")
                    print(self.cam0_handler.refresh_camera_list())
                    break
            if ret1 is True:
                self.cam1_stream.send_to_all(frame0)
            if self.state is States.WAITING:  # Prints detected data (testing)
                _, speeds = self.waiting_state.run_calculation(frame0)

            elif self.state is States.PARKING:
                _, path_data = self.driving_state.run_calculation(frame0)
                self.check_actions(path_data)

            elif self.state is States.DRIVING:
                _, path_data = self.driving_state.run_calculation(frame0)
                self.check_actions(path_data)

            elif self.state is States.STOPPING:
                count, speeds = self.stopping_state.run_calculation(frame0)
                if count == 0:
                    speeds = {
                        "dir_0": 0,
                        "dir_1": 0,
                        "speed_0": 10,
                        "speed_1": 10
                    }
                self.car_comm.set_motor_speed(speeds["dir_0"], speeds["speed_0"],
                                              speeds["dir_1"], speeds["speed_1"])
            elif self.state is States.MANUAL:
                _, speeds = ManualDriving.run_calculation(
                    self.joystick_position)
                self.car_comm.set_motor_speed(speeds["dir_0"], speeds["speed_0"],
                                              speeds["dir_1"], speeds["speed_1"])

            elif self.state is States.STEREO:
                if frame0 is not None and frame1 is not None:
                    depth_val = self.stereo_vision.run_calculation([frame0, frame1])
                    if depth_val < 500:
                        speeds = {
                        "dir_0": 0,
                        "dir_1": 0,
                        "speed_0": 0,
                        "speed_1": 0
                        }
                        self.car_comm.set_motor_speed(speeds["dir_0"], speeds["speed_0"],
                                                      speeds["dir_1"], speeds["speed_1"])
            elif self.state == States.SHUTDOWN:
                self.car_comm.stop()
                break

    def check_actions(self, path_data):
        '''Check actions for driving data'''
        if path_data is not None:
            angles = path_data['angles']
            times = path_data['times']
            self.actions: deque = deque()
            for angle, action_time in zip(angles, times):
                self.actions.append({
                    'speed': self.conf['spline']['velocity'],
                    'angle': angle,
                    'time': action_time,
                })
                path_data = None

        time_now = self.prev_action['time'] - time.time()
        # pylint: disable=E1136
        if self.actions is not None or \
            (self.cur_action is not None and time_now >= self.cur_action['time']) or \
            self.cur_action is None:
            self.cur_action = self.actions.popleft() if self.actions else None

        if self.cur_action is None or \
            (self.cur_action is not None and time_now >= self.cur_action['time']):
            angle = 0
            speed = 0
        else:
            angle = self.cur_action['angle']
            speed = self.cur_action['speed']

        if self.prev_action['speed'] != speed and self.prev_action['angle'] != angle:
            self.car_comm.drive_direction(speed, angle)
            self.prev_action['speed'] = speed
            self.prev_action['angle'] = angle
            self.prev_action['time'] = time.time()
