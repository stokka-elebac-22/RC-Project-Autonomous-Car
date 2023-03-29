'''Main'''
import pygame as pg
from pygame.locals import QUIT # pylint: disable=no-name-in-module
from environment import Environment
from display import DisplayEnvironment
from a_star import AStar

if __name__ == '__main__': # pylint: disable=R0801
    SIZE = (10, 11)
    W_SIZE = 600
    WINDOW_SIZE = (W_SIZE* (SIZE[1]/SIZE[0]), W_SIZE)

    # create the environment and adding the 'car'
    env= Environment(SIZE, 1, {'view_point': None, 'object_id': 10})
    display = DisplayEnvironment(WINDOW_SIZE, SIZE)

    env.insert((2, SIZE[1]-2), 20)

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

        start_pos_path = env.get_pos(10)
        end_pos_path = env.get_pos(20)
        cur_mat = env.get_data()
        display.update(cur_mat)
        cur_mat = env.get_data()
        ret, path = AStar().get_data(cur_mat, start_pos_path, end_pos_path)

        if ret:
            for pos in path[1:-1]:
                display.insert(pos, 'Path')

        display.display()
