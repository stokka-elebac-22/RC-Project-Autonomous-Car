'''Main'''
import pygame as pg
from pygame.locals import QUIT # pylint: disable=no-name-in-module
from environment.src.environment import Environment
from environment.src.display import DisplayEnvironment
from environment.src.a_star import AStar
from environment.src.a_star_display import AStar as AstarDisplay
from qr_code.qr_code import QRCode

if __name__ == '__main__':
    SIZE = (10, 11)
    W_SIZE = 600
    WINDOW_SIZE = (W_SIZE* (SIZE[1]/SIZE[0]), W_SIZE)

    QR_SIZE_PX = 120
    QR_SIZE_MM = 52
    QR_DISTANCE = 320
    qr_code = QRCode(QR_SIZE_PX, QR_SIZE_MM, QR_DISTANCE)
    CAMERA_ID = 0
    CAMERA_PX_SIZE = (1920, 1080)
    # print('Setting up camera...')
    # cap = cv.VideoCapture(CAMERA_ID)
    # print('Done')
    DELAY = 1

    # create the environment and adding the 'car'
    env= Environment(SIZE, 70, {'view_point': None, 'object_id': 10})
    display = DisplayEnvironment(WINDOW_SIZE, SIZE)

    a_star = AStar()
    a_star_display = AstarDisplay(10, 1)

    env.insert_by_index((1,1), 11)

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

        # ret, frame = cap.read()
        # if not ret:
        #     break
        # qr_data = qr_code.get_data(frame)
        # if qr_data['ret']:
        #     env.remove(11)
        #     # using only the first qr code
        #     distance_y = qr_data['distances'][0]
        #     points = qr_data['points'][0]
        #     width = qr_code.qr_geometries[0].get_width()
        #     mm_per_px = QR_SIZE_MM/width
        #     if points[0][0] > CAMERA_PX_SIZE[0]/2:
        #         offset = points[0][0] - CAMERA_PX_SIZE[1]/2
        #     else:
        #         offset = points[1][0] - CAMERA_PX_SIZE[1]/2
        #     distance_x = offset * mm_per_px + 200 # idk why 200,

        #     env.insert((distance_x, distance_y), 11)

        start_pos_path = env.get_pos(10)
        end_pos_path = env.get_pos(11)

        cur_mat = env.get_data()
        display.update(cur_mat)
        cur_mat = env.get_data()
        ret, path = a_star.get_data(cur_mat, start_pos_path, end_pos_path)

        if ret:
            for pos in path[1:-1]:
                display.insert(pos, 'Path')

        display.display()
