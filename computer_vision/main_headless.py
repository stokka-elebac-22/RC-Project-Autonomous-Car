'''main_headless.py: DATBAC23 Car system main.'''
import time
from typing import List
from collections import deque
from defines import States, MessageId, ActionsDict
from socket_handling.abstract_server import NetworkSettings
from socket_handling.multi_socket_server import MultiSocketServer
from camera_handler.camera_headless import CameraHandler
from camera_handler.camera_sock_server import CamSocketStream
from car_communication.abstract_communication import AbstractCommunication
from car_communication.can_bus_communication import CanBusCommunication
from car_communication.car_serial_communication import CarSerialCommunication
from car_communication.car_stepper_communication import CarStepperCommunication
from module_setup import ModuleSetup
from driving.driving_states import DrivingStates

class Headless():  # pylint: disable=R0903
    '''Class handling headless running'''
    # pylint: disable=R0902
    # pylint: disable=R0915
    def __init__(self, conf: dict): # pylint: disable=R0912
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
        cameras = self.cam0_handler.refresh_camera_list()

        self.module_setup = ModuleSetup(conf)
        self.traffic_sign_detector = self.module_setup.traffic_sign_detector_setup()
        self.lane_detector = self.module_setup.lane_detector_setup()
        self.qr_code = self.module_setup.qr_code_setup()
        self.parking_slot_detector = self.module_setup.parking_slot_detector_setup()
        self.pathfinding = self.module_setup.pathfinding_setup()

        self.driving_states = DrivingStates(
            conf=conf,
            pathfinding=self.pathfinding,
            qr_code=self.qr_code,
            stop_sign_detector=self.traffic_sign_detector,
            parking_slot_detector=self.parking_slot_detector,
            lane_detector=self.lane_detector
        )

        self.actions: List[ActionsDict] = deque()
        self.cur_action = None
        self.prev_action = {
            'angle': None,
            'speed': None,
            'time': time.time(),
        }


        while True:
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

            if self.state == States.WAITING:
                actions: List[ActionsDict] = self.driving_states.waiting(frame0)
            elif self.state == States.DRIVING:
                actions: List[ActionsDict] = self.driving_states.driving(
                    frame0, cameras[conf["camera0"]["id"]].get_dimensions())
            elif self.state == States.STOPPING:
                actions: List[ActionsDict] = self.driving_states.stopping(frame0)
            elif self.state == States.PARKING:
                actions: List[ActionsDict] = self.driving_states.parking(
                    frame0, cameras[conf["camera0"]["id"]].get_dimensions())
            elif self.state is States.MANUAL:
                pass

            if actions is not None:
                self.actions = actions

            time_now = self.prev_action['time'] - time.time()
            # pylint: disable=E1136
            if actions is not None or \
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
