'''Driving class'''

import cv2 as cv
from driving.driving_states import DrivingStates
from driving.driving_setup import DrivingSetup
try:
    from computer_vision.camera_handler.camera_handler import CameraHandler
    from computer_vision.camera_handler.camera import Camera
    from computer_vision.environment.src.a_star import AStar
    from computer_vision.environment.src.environment import Environment, ViewPointObject
    from computer_vision.pathfinding.pathfinding import PathFinding
    from computer_vision.qr_code.qr_code import QRCode, QRSize
    from computer_vision.line_detection.lane_detection import LaneDetector
    from computer_vision.line_detection.parking_slot_detection import ParkingSlotDetector
    from computer_vision.traffic_sign_detection.traffic_sign_detector import TrafficSignDetector
    from computer_vision.car_communication.abstract_communication import AbstractCommunication
    from computer_vision.car_communication.can_bus_communication import CanBusCommunication
    from computer_vision.car_communication.car_serial_communication import CarSerialCommunication
    from computer_vision.socket_handling.abstract_server import NetworkSettings
    from computer_vision.socket_handling.multi_socket_server import MultiSocketServer
    from computer_vision.camera_handler.camera_headless import CameraHandler
    from computer_vision.camera_handler.camera_sock_server import CamSocketStream
except ImportError:
    from camera_handler.camera_handler import CameraHandler
    from camera_handler.camera import Camera
    from camera_handler.camera_headless import CameraHandler
    from camera_handler.camera_sock_server import CamSocketStream
    from environment.src.a_star import AStar
    from environment.src.environment import Environment, ViewPointObject
    from pathfinding.pathfinding import PathFinding
    from qr_code.qr_code import QRCode, QRSize
    from line_detection.lane_detection import LaneDetector
    from line_detection.parking_slot_detection import ParkingSlotDetector
    from traffic_sign_detection.traffic_sign_detector import TrafficSignDetector
    from car_communication.abstract_communication import AbstractCommunication
    from car_communication.can_bus_communication import CanBusCommunication
    from car_communication.car_serial_communication import CarSerialCommunication
    from socket_handling.abstract_server import NetworkSettings
    from socket_handling.multi_socket_server import MultiSocketServer

class ModuleSetup: # pylint: disable=R0903
    '''
    The class for setting up modules
    '''
    def __init__(self, conf: dict) -> None:
        self.conf = conf

    def pathfinding_setup(self):
        '''Init Pathfinding'''
        # ----- INIT PARKFINDING ALGORITHM ----- #
        a_star = AStar(self.conf['a_star']['weight'], self.conf['a_star']['penalty'])

        # ----- INIT ENVIRONMENT ----- #
        view_point_object: ViewPointObject = {
            'view_point': None, # will be calculated in the environment class
            'object_id': self.conf['object_id']['car'],
        }

        if self.conf['simulation']['live']:
            frame_width, frame_height = self.cam.get_dimensions()
        else:
            img = cv.imread(self.conf['simulation']['image_paths']['camera_view'])
            frame_width, frame_height, _ = img.shape
        environment: Environment = Environment(
            self.conf['environment']['size'],
            (frame_width, frame_height),
            self.conf['environment']['real_size'],
            view_point_object,
        )

        # ----- INIT PATHFINDING ----- #
        pathfinding: PathFinding = PathFinding(
            environment=environment,
            pathfinding_algorithm=a_star,
            velocity=self.conf['spline']['velocity']
        )
        return pathfinding

    def qr_code_setup(self):
        '''Init QR'''

        print('Setting up QR code...')
        # ----- INIT QR CODE ----- #
        qr_size: QRSize = {
            'px': self.conf['qr_code_size']['px'],
            'mm': self.conf['qr_code_size']['mm'],
            'distance': self.conf['qr_code_size']['distance'],
        }
        qr_code = QRCode(qr_size)
        return qr_code

    def parking_slot_detector_setup(self):
        '''Init Parking Slot Detector'''
        parking_slot_detector = ParkingSlotDetector(
            canny=self.conf['parking_slot_detector']['canny'],
            hough=self.conf['parking_slot_detector']['hough'],
            blur=self.conf['parking_slot_detector']['blur'],
            iterations=self.conf['parking_slot_detector']['iterations'],
            filter_atol=self.conf['parking_slot_detector']['canny'],
        )
        return parking_slot_detector

    def lane_detector_setup(self):
        '''Init Lane Detector'''
        lane_detector = LaneDetector(
            canny=self.conf['lane_detector']['canny'],
            blur=self.conf['lane_detector']['blur'],
            hough=self.conf['lane_detector']['hough'],
            width=self.conf['lane_detector']['width']
        )
        return lane_detector

    def traffic_sign_detector_setup(self):
        '''Init Traffic Sign Detector'''
        traffic_size: QRSize = {
            'px': self.conf['sign_size']['px'],
            'mm': self.conf['sign_size']['mm'],
            'distance': self.conf['sign_size']['distance'],
        }
        min_size_traffic = self.conf['traffic_sign_detector']['min_size']
        stop_sign_detector = TrafficSignDetector('cascade.xml',
                                                      traffic_size,
                                                      (min_size_traffic[0], min_size_traffic[1]))
        return stop_sign_detector