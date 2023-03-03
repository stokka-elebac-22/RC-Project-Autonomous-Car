'''
The main file for the driving logic.
This file should only contain short code
'''

import sys
import os
from lib import get_available_cameras
import cv2 as cv
import yaml

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# pylint: disable=C0413
from computer_vision.qr_code.qr_code import QRCode, QRSize
from computer_vision.environment.src.environment import Environment
from computer_vision.environment.src.lib import Objects
from computer_vision.environment.src.a_star import AStar

# ---------- CONSTANTS ---------- #

# ---------- MAIN ---------- #
if __name__ == '__main__':
    # ---------- INIT ---------- #
    ### init camera ###
    # need to run this command to get VideoCapture to work after every restart of pi
    os.system('sudo chmod 777 /dev/video0')

    # open yaml file
    with open('driving/config.yaml', 'r', encoding='utf8') as file:
        config = yaml.safe_load(file)

    ret, available_cameras = get_available_cameras()

    if not ret:
        sys.stdout.write('There is no available cameras')
        raise ConnectionError

    sys.stdout.write(f'Connecting to camera {available_cameras[0]}')
    camera = cv.VideoCapture(available_cameras[0])

    ### init environment ###
    SIZE = (config['environment']['sizex'], config['environment']['sizey'])
    WINDOW_WIDTH = config['gui']['window_width']
    WINDOW_SIZE = (WINDOW_WIDTH* (SIZE[1]/SIZE[0]), WINDOW_WIDTH)
    env= Environment(SIZE, 1, {'object_id': 10})
    objects = Objects()

    ### init qr code ###
    QR_SIZE: QRSize = {
        'px': config['qr_code_size']['px'],
        'mm': config['qr_code_size']['mm'],
        'distance': config['qr_code_size']['distance'],
    }
    qr_code = QRCode(QR_SIZE)
    qr_code_id = objects.get_data('QR').id

    # ---------- LOOP ---------- #
    while True:
        # ---------- GET CAMERA INFORMATION---------- #
        ret, frame = camera.read()
        if not ret:
            continue

        ### QR Code ###
        qr_data = qr_code.get_data(frame)
        if not qr_data['ret']:
            continue

        # insert the qr codes to the environment
        for i in range(len(qr_data['info'])):
            env.insert(qr_data['distances'][i], qr_code_id)

        # ---------- UPDATE ENVIRONMENT ---------- #
        start_pos_path = env.get_pos(10)
        end_pos_path = env.get_pos(11)
        cur_mat = env.get_data()

        # ---------- PATH ---------- #
        ret, path = AStar().get_data(cur_mat, start_pos_path, end_pos_path)

        # ---------- ACTION ---------- #
