'''
The main file for the driving simulation
'''
import os
import sys
import yaml
from driving import Driving
from driving_setup import DrivingSetup
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
# pylint: disable=C0413
from computer_vision.camera_handler.camera_handler import CameraHandler
from computer_vision.camera_handler.camera import Camera
from computer_vision.pathfinding.pathfinding import PathFinding
from computer_vision.environment.src.a_star import AStar
from computer_vision.environment.src.environment import Environment
from computer_vision.qr_code.qr_code import QRSize, QRCode

CONFIG_FILE = 'driving_simulation/config'

if __name__ == '__main__':
    # ----- CONFIG ----- #
    with open(CONFIG_FILE + '.yml', 'r', encoding='utf8') as f:
        try:
            conf = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

    # ----- CAMERAS ----- #
    print('Setting up cameras...')
    camera_handler = CameraHandler()
    cameras = camera_handler.refresh_camera_list()
    # finding the resolution
    RESOLUTION = None
    if conf['camera']['active'] == 'web':
        RESOLUTION = conf['camera']['camera_resolution']['web']
    elif conf['camera']['active'] == 'logi':
        RESOLUTION = conf['camera']['camera_resolution']['logi']

    if RESOLUTION is None:
        cam = Camera(cameras[0]['id'])
    else:
        cam = Camera(cameras[0]['id'], RESOLUTION)

    ret, frame = cam.read()
    if not ret:
        raise ConnectionError

    # ----- INIT PARKFINDING ALGORITHM ----- #
    a_star = AStar(conf['a_star']['weight'], conf['a_star']['penalty'])

    # ----- INIT ENVIRONMENT ----- #
    environment: Environment = Environment(
        conf['environment']['size'],
        conf['environment']['real_size'],
        {'object_id': 10},
    )

    # ----- INIT PATHFINDING ----- #
    frame_width, frame_height = cam.get_dimensions()
    path_finding: PathFinding = PathFinding(
        pixel_size=(frame_width, frame_height),
        environment=environment,
        pathfinding_algorithm=a_star,
    )

    # ----- INIT QR CODE ----- #
    qr_size: QRSize = {
        'px': conf['qr_code_size']['px'],
        'mm': conf['qr_code_size']['mm'],
        'distance': conf['qr_code_size']['distance'],
    }
    qr_code = QRCode(qr_size)

    # ----- DRIVING ----- #
    print('Start running...')
    driving = Driving(
        conf=conf,
        pathfinding=path_finding,
        qr_code=qr_code)
    driving_setup = DrivingSetup(
        conf=conf,
        driving=driving,
        camera=cam,
        image_paths=conf['image_paths'])
    driving_setup.run()
