'''
The main file for the driving logic.
This file should only contain short code
'''
from typing import Tuple, List
from computer_vision.qr_code.qr_code import QRCode
from computer_vision.environment.src.environment import Environment
from computer_vision.camera_handler.camera import Camera
from computer_vision.camera_handler.camera_handler import CameraHandler

# ---------- CONSTANTS ---------- #

# ---------- MAIN ---------- #
if __name__ == '__main__':
    # ---------- INIT ---------- #
    ### init camera ###
    ### init qr code ###
    QR_CODE_SIZE_PX = 76
    QR_CODE_SIZE_MM = 52
    QR_CODE_DISTANCE = 500
    size = {
        'px': QR_CODE_SIZE_PX,
        'mm': QR_CODE_SIZE_MM,
        'distance': QR_CODE_DISTANCE
    }
    qr_code = QRCode(size)
    ### init environment ###
    SIZE = (10, 11)
    WINDOW_WIDTH = 600
    WINDOW_SIZE = (WINDOW_WIDTH* (SIZE[1]/SIZE[0]), WINDOW_WIDTH)
    env= Environment(SIZE, 1, {'object_id': 10})

    camera_handler = CameraHandler()
    camera_handler.refresh_camera_list()
    available_cameras = camera_handler.get_camera_list()

    # assuming the first camera is the correct one
    CAMERA = None
    if len(available_cameras) != 0:
        camera_id = available_cameras[0].get('id')
        # CAMERA = Camera(camera_id)

    # ---------- LOOP ---------- #
    while True:
        # ---------- GET CAMERA INFORMATION---------- #
        # The environment objects is a list of tuples with
        # an object id, x distance and y distance
        env_objects: List[Tuple[int, int, int]] = []

        ### QR Code ###
        # qr_code.get_data(frame)

        ### Traffic Sign ###

        ### Line detection ###

        # ---------- UPDATE ENVIRONMENT ---------- #
        # Insert objects into the environment
        for obj in env_objects:
            env.insert((env_objects[1], env_objects[2]),
                env_objects[0])

        # ---------- ACTION ---------- #
