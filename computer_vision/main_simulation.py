'''
The main file for the driving simulation
'''
import os
import yaml
import cv2 as cv
from simulation.driving import Driving
from simulation.driving_setup import DrivingSetup
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
except ImportError:
    from camera_handler.camera_handler import CameraHandler
    from camera_handler.camera import Camera
    from environment.src.a_star import AStar
    from environment.src.environment import Environment, ViewPointObject
    from pathfinding.pathfinding import PathFinding
    from qr_code.qr_code import QRCode, QRSize
    from line_detection.lane_detection import LaneDetector
    from line_detection.parking_slot_detection import ParkingSlotDetector
    from traffic_sign_detection.traffic_sign_detector import TrafficSignDetector

class Simulation: # pylint: disable=R0903
    '''
    The class for running the simulation
    '''
    def __init__(self, conf: dict) -> None:
        self.conf = conf
        self.cam = None
        if self.conf['simulation']['live']:
            self.cam = self.__camera_setup()
        pathfinding = self.__pathfinding_setup()
        qr_code = self.__qr_code_setup()
        parking_slot_detector = self.__parking_slot_detector_setup()
        lane_detector = self.__lane_detector_setup()
        traffic_sign_detector = self.__traffic_sign_detector_setup()

        # ----- DRIVING ----- #
        driving = Driving(
            conf=conf,
            pathfinding=pathfinding,
            qr_code=qr_code,
            parking_slot_detector=parking_slot_detector,
            lane_detector=lane_detector,
            stop_sign_detector=traffic_sign_detector)
        self.driving_setup = DrivingSetup(
            conf=conf,
            driving=driving,
            camera=self.cam)
        self.run()

    def __camera_setup(self):
        # ----- CAMERAS ----- #
        print('Setting up cameras...')
        camera_handler = CameraHandler()
        cameras = camera_handler.refresh_camera_list()
        # finding the resolution
        resolution = None
        if self.conf['camera']['active'] == 'web':
            resolution = self.conf['camera']['camera_resolution']['web']
        elif self.conf['camera']['active'] == 'logi':
            resolution = self.conf['camera']['camera_resolution']['logi']

        if resolution is None:
            cam = Camera(cameras[0]['id'])
        else:
            cam = Camera(cameras[0]['id'], resolution)
        ret, _ = cam.read()
        if not ret:
            raise ConnectionError
        return cam

    def __pathfinding_setup(self):
        print('Setting up pathfinding...')
        # ----- INIT PARKFINDING ALGORITHM ----- #
        a_star = AStar(self.conf['a_star']['weight'], self.conf['a_star']['penalty'])

        # ----- INIT ENVIRONMENT ----- #
        view_point_object: ViewPointObject = {
            'view_point': None, # will be calculated in the environment class
            'object_id': self.conf['object_id']['car'],
        }
        environment: Environment = Environment(
            self.conf['environment']['size'],
            self.conf['environment']['real_size'],
            view_point_object,
        )

        # ----- INIT PATHFINDING ----- #
        if self.conf['simulation']['live']:
            frame_width, frame_height = self.cam.get_dimensions()
        else:
            img = cv.imread(self.conf['simulation']['image_paths']['camera_view'])
            frame_width, frame_height, _ = img.shape
        pathfinding: PathFinding = PathFinding(
            pixel_size=(frame_width, frame_height),
            environment=environment,
            pathfinding_algorithm=a_star,
            velocity=self.conf['spline']['velocity']
        )
        return pathfinding

    def __qr_code_setup(self):
        print('Setting up QR code...')
        # ----- INIT QR CODE ----- #
        qr_size: QRSize = {
            'px': self.conf['qr_code_size']['px'],
            'mm': self.conf['qr_code_size']['mm'],
            'distance': self.conf['qr_code_size']['distance'],
        }
        qr_code = QRCode(qr_size)
        return qr_code
    
    def __parking_slot_detector_setup(self):
        parking_slot_detector = ParkingSlotDetector(
            canny=self.conf['parking_slot_detector']['canny'],
            hough=self.conf['parking_slot_detector']['hough'],
            blur=self.conf['parking_slot_detector']['blur'],
            iterations=self.conf['parking_slot_detector']['iterations'],
            filter_atol=self.conf['parking_slot_detector']['canny'],
        )
        return parking_slot_detector

    def __lane_detector_setup(self):
        lane_detector = LaneDetector(
            canny=self.conf['lane_detector']['canny'],
            blur=self.conf['lane_detector']['blur'],
            hough=self.conf['lane_detector']['hough'],
            width=self.conf['lane_detector']['width']
        )
        return lane_detector

    def __traffic_sign_detector_setup(self):
        traffic_size: QRSize = {
            'px': self.conf['sign_size']['px'],
            'mm': self.conf['sign_size']['mm'],
            'distance': self.conf['sign_size']['distance'],
        }
        min_size_traffic = self.conf['traffic_sign']['min_size']
        stop_sign_detector = TrafficSignDetector('cascade.xml',
                                                      traffic_size,
                                                      min_size_traffic)
        return stop_sign_detector


    def run(self):
        '''Run the simulation'''
        print('Running...')
        self.driving_setup.run()


if __name__ == '__main__':
    CONFIG_FILE = 'config'
    print('Reading configuration file...')
    # ----- CONFIG ----- #
    with open(CONFIG_FILE + '.yml', 'r', encoding='utf8') as f:
        try:
            c = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

    # ----- TEST IF PATHS ARE CORRECT ----- #
    if c['simulation']['active']:
        image_paths = c['simulation']['image_paths']
        for image_path in [image_paths['camera_view'], image_paths['arrow']]:
            if not os.path.exists(image_path):
                raise FileNotFoundError

    simulation = Simulation(c)
    simulation.run()
