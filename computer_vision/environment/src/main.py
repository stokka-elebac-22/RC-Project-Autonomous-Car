'''Main'''
import pygame as pg
from pygame.locals import QUIT # pylint: disable=no-name-in-module
from environment import Environment
from display import DisplayEnvironment
from a_star import AStar

if __name__ == '__main__':
    SIZE = (10, 10)
    WINDOW_SIZE = (500, 500)
    environment = Environment(SIZE, 1)
    display = DisplayEnvironment(WINDOW_SIZE, SIZE)

    # adding the 'car'
    environment.insert_object(9, 5, )

    RUN = True
    while RUN:
        for event in pg.event.get():
            if event.type == QUIT:
                RUN = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    environment.insert_object(5, 0, 1)

        cur_mat = environment.get_data()
        path = AStar().get_data(cur_mat, (1, 1), (9, 4))

        print(path)

        for values in path[1:-1]:
            display.insert(values, 'Path')

        display.update(cur_mat)
