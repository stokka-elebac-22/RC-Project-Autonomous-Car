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
from computer_vision.qr_code.qr_code import QRCode, QRSize


# ---------- CONSTANTS ---------- #

# ---------- MAIN ---------- #
if __name__ == '__main__':
    # ---------- INIT ---------- #
    ### init camera ###
    # need to run this command to get VideoCapture to work after every restart of pi
    os.system('sudo chmod 777 /dev/video0')

    ret, available_cameras = get_available_cameras()

    if not ret:
        sys.stdout.write('There is no available cameras')
        raise ConnectionError

    sys.stdout.write(f'Connecting to camera {available_cameras[0]}')
    camera = cv.VideoCapture(available_cameras[0])

    ### init qr code ###
    QR_SIZE: QRSize = {
        'px': 76,
        'mm': 52,
        'distance': 500
    }
    qr_code = QRCode(QR_SIZE)

    ### init environment ###
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

        sys.stdout.write(f'QR Code: \n \
                    Distance: {qr_data["distances"][0]} \n \
                    Angle: {qr_data["angles"][0]} \
                   ')


        ### Line detection ###

        # ---------- UPDATE ENVIRONMENT ---------- #

        # ---------- ACTION ---------- #
