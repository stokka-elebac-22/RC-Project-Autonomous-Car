'''Main'''
import pygame as pg
from pygame.locals import QUIT # pylint: disable=no-name-in-module
from environment import Environment
from display import DisplayEnvironment
from a_star import AStar

if __name__ == '__main__':
    SIZE = (10, 11)
    WINDOW_SIZE = (660, 600)
    # create the environment and adding the 'car'
    env= Environment(SIZE, 1, {'view_point': None, 'object_id': 10})
    display = DisplayEnvironment(WINDOW_SIZE, SIZE)

    env.insert_object((-2, 6), 11)

    RUN = True
    while RUN:
        for event in pg.event.get():
            if event.type == QUIT:
                RUN = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    pass

        start_pos_path = env.get_pos(10)
        end_pos_path = env.get_pos(11)
        cur_mat = env.get_data()
        display.update(cur_mat)
        ret, path = AStar().get_data(cur_mat, start_pos_path, end_pos_path)

        if ret:
            for pos in path[1:-1]:
                display.insert(pos, 'Path')

        display.display()