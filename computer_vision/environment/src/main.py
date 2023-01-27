'''Main'''
import pygame as pg
from pygame.locals import QUIT # pylint: disable=no-name-in-module
from environment import Environment
from display import DisplayEnvironment
from a_star import AStar

import cv2 as cv
from ...qr_code.qr_code import QRCode

if __name__ == '__main__':
    SIZE = (10, 11)
    W_SIZE = 600
    WINDOW_SIZE = (W_SIZE* (SIZE[1]/SIZE[0]), W_SIZE)

    # QR Code measured, 55mm lense
    QR_SIZE_PX = 120
    QR_SIZE_MM = 52
    QR_DISTANCE = 320
    qr_code = QRCode(QR_SIZE_PX, QR_SIZE_MM, QR_DISTANCE)
    CAMERA_ID = 0
    cap = cv.VideoCapture(CAMERA_ID)
    DELAY = 1

    # create the environment and adding the 'car'
    env= Environment(SIZE, 1, {'view_point': None, 'object_id': 10})
    display = DisplayEnvironment(WINDOW_SIZE, SIZE)

    env.insert((2, SIZE[1]-2), 11)

    RUN = True
    while RUN:
        for event in pg.event.get():
            if event.type == QUIT:
                RUN = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                TILE_SIZE = WINDOW_SIZE[1]/SIZE[0]
                col = mouse_pos[0] // TILE_SIZE
                row = mouse_pos[1] // TILE_SIZE
                env.insert_by_index((int(row), int(col)), '1')

        ret, frame = cap.read()
        if not ret:
            break
        qr_data = qr_code.get_data(frame)
        

        start_pos_path = env.get_pos(10)
        end_pos_path = env.get_pos(11)
        cur_mat = env.get_data()
        display.update(cur_mat)
        cur_mat = env.get_data()
        print(cur_mat)
        ret, path = AStar().get_data(cur_mat, start_pos_path, end_pos_path)

        if ret:
            for pos in path[1:-1]:
                display.insert(pos, 'Path')

        display.display()
