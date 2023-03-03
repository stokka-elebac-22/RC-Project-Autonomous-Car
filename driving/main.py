'''
The main file for the driving logic.
This file should only contain short code
'''

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# pylint: disable=C0413
from computer_vision.camera_handler.camera_handler import CameraHandler
from computer_vision.camera_handler.camera import Camera


# ---------- CONSTANTS ---------- #

# ---------- MAIN ---------- #
if __name__ == '__main__':
    # ---------- INIT ---------- #
    ### init camera ###
    camera_handler = CameraHandler()
    camera_handler.refresh_camera_list()
    available_cameras = camera_handler.get_camera_list()

    if len(available_cameras) == 0:
        sys.stdout.write('There is no available cameras')
        raise ConnectionError

    CAMERA_STRING = 'Cameras: \n'
    for camera in available_cameras:
        CAMERA_STRING += camera_handler.get_camera_string(camera['id'])

    sys.stdout.write(CAMERA_STRING)

    camera = Camera(available_cameras[0]['id'])

    ### init qr code ###
    ### init environment ###
    # ---------- LOOP ---------- #
    while True:
        sys.stdout.write('The code is running.')
        # ---------- GET CAMERA INFORMATION---------- #
        ### QR Code ###
        # qr_code.get_data(frame)

        ### Line detection ###

        # ---------- UPDATE ENVIRONMENT ---------- #

        # ---------- ACTION ---------- #
