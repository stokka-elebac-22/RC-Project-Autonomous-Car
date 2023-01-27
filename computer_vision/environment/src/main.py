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
    environment = Environment(SIZE, 1, {'view_point': None, 'object_id': 10})
    display = DisplayEnvironment(WINDOW_SIZE, SIZE)

    environment.insert_object((0, 8), 11)

    RUN = True
    while RUN:
        for event in pg.event.get():
            if event.type == QUIT:
                RUN = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    pass

        cur_mat = environment.get_data()
        path = AStar().get_data(cur_mat, (1, 1), (9, 4))

        for values in path[1:-1]:
            display.insert(values, 'Path')

        display.update(cur_mat)
