'''
The main file for the driving logic.
This file should only contain short code
'''

import sys
import os
from lib import get_available_cameras
import cv2 as cv

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# pylint: disable=C0413


# ---------- CONSTANTS ---------- #

# ---------- MAIN ---------- #
if __name__ == '__main__':
    # ---------- INIT ---------- #
    ### init camera ###

    ret, available_cameras = get_available_cameras()

    if not ret:
        sys.stdout.write('There is no available cameras')
        raise ConnectionError

    sys.stdout.write(f'Connecting to camera {available_cameras[0]}')
    camera = cv.VideoCapture(available_cameras[0])

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
