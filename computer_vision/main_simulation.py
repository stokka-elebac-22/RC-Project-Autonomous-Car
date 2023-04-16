'''
The main file for the driving simulation
'''
import os
import sys
import yaml
<<<<<<< HEAD
from pynput import keyboard
from driving.driving import Driving
=======
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
except ImportError:
    from camera_handler.camera_handler import CameraHandler
    from camera_handler.camera import Camera
    from environment.src.a_star import AStar
    from environment.src.environment import Environment, ViewPointObject
    from pathfinding.pathfinding import PathFinding
    from qr_code.qr_code import QRCode, QRSize

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

        # ----- DRIVING ----- #
        driving = Driving(
            conf=conf,
            pathfinding=pathfinding,
            qr_code=qr_code)
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

    def run(self):
        '''Run the simulation'''
        print('Running...')
        self.driving_setup.run()

>>>>>>> 74c1c7426b705f5b5b7fcb59330a8506d9164cdc

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

    # ----- INTERRUPTS ----- #
    def on_press(key):
        '''on_press'''
        if key == keyboard.Key.esc:
            sys.exit()

    # Collect events until released
    listener = keyboard.Listener(
        on_press=on_press
    )
    listener.start()


    simulation = Driving(c)
    simulation.run()
