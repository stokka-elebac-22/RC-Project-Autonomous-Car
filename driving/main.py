'''
The main file for the driving logic.
This file should only contain short code
'''

import sys
import os
from typing import List
from lib import get_available_cameras, get_cam_center, get_qr_code_distance
import yaml
import cv2 as cv

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# pylint: disable=C0413
from computer_vision.qr_code.qr_code import QRCode, QRSize
from computer_vision.environment.src.environment import Environment
from computer_vision.environment.src.lib import Objects
from computer_vision.environment.src.a_star import AStar
from computer_vision.pathfinding.spline import catmull_rom_chain
from computer_vision.pathfinding.lib import angle_and_velocity_from_derivative
from computer_vision.pathfinding.pathfinding import PathFinding

# ---------- CONSTANTS ---------- #

# ---------- MAIN ---------- #
if __name__ == '__main__':
    # ---------- INIT ---------- #
    ### init camera ###
    # need to run this command to get VideoCapture to work after every restart of pi
    os.system('sudo chmod 777 /dev/video0')

    # open yaml file
    with open('config.yaml', 'r', encoding='utf8') as file:
        config = yaml.safe_load(file)

    ret, available_cameras = get_available_cameras()

    if not ret:
        sys.stdout.write('There is no available cameras\n')
        raise ConnectionError

    sys.stdout.write(f'Connecting to camera {available_cameras[0]}\n')
    camera = cv.VideoCapture(available_cameras[0])
    # test if the camera gives out frame
    ret, _ = camera.read()
    if not ret:
        raise ConnectionError
    sys.stdout.write('Connected\n')

    # ---------- INIT ENVIRONMENT ---------- #
    SIZE = config['environment']['size']
    WINDOW_WIDTH = config['gui']['window_width']
    WINDOW_SIZE = (WINDOW_WIDTH* (SIZE[1]/SIZE[0]), WINDOW_WIDTH)
    env= Environment(SIZE, 1, {'object_id': 10})
    objects = Objects()

    # ---------- INIT PATHFINDING ALGORITHM ---------- #
    a_star = AStar(config['a_star']['weight'], config['a_star']['penalty'])

    # ---------- INIT PATHFINDING ---------- #
    # finding the center of the camera

    _, frame = camera.read()
    cam_center = get_cam_center(frame)
    path_finding = PathFinding(
        pixel_size=config['pathfinding']['pixel_size'],
        cam_size=config['pathfinding']['cam_size'],
        cam_center=cam_center,
        environment=env,
        pathfinding_algorithm=a_star
    )

    # ---------- INIT QR CODE ---------- #
    QR_SIZE: QRSize = {
        'px': config['qr_code_size']['px'],
        'mm': config['qr_code_size']['mm'],
        'distance': config['qr_code_size']['distance'],
    }
    qr_code = QRCode(QR_SIZE)
    QR_CODE_ID = objects.get_data('QR').id
    CAR_ID = objects.get_data('Car').id

    # ---------- LOOP ---------- #
    while True:
        # ---------- INIT ---------- #
        objects: List[path_finding.Objects] = []

        # ---------- GET CAMERA INFORMATION---------- #
        ret, frame = camera.read()
        if not ret:
            continue

        ### QR Code ###
        qr_data = qr_code.get_data(frame)
        if not qr_data['ret']:
            continue

        # add qr code to the objects list

        qr_code_distances = get_qr_code_distance(qr_data, path_finding)

        path_finding_object: path_finding.Objects = {
            'values': qr_code_distances,
            'distance': True,
            'object_id': QR_CODE_ID
        }

        objects.append(path_finding_object)

        # ---------- UPDATE ENVIRONMENT ---------- #
        path_finding.environment.reset()
        path_finding.insert_objects(objects)

        start_pos_path = path_finding.environment.get_pos(CAR_ID)
        end_pos_path = path_finding.environment.get_pos(QR_CODE_ID)
        cur_mat = path_finding.environment.get_data()

        # ---------- PATH ---------- #
        path = a_star.get_data(cur_mat, start_pos_path, end_pos_path)

        # ---------- SPLINES ---------- #
        if ret:
            curve, derivative = catmull_rom_chain(path, config['spline']['tension'])
            angles, velocity = angle_and_velocity_from_derivative(derivative)

            sys.stdout.write(f'angle: {angles[0]}\n\
                    velocity:{velocity[0]}\n\n')

        # ---------- ACTION ---------- #
