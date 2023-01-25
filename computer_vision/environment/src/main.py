'''Main'''
import pygame as pg
from pygame.locals import QUIT # pylint: disable=no-name-in-module
from environment import Environment
from display import DisplayEnvironment

if __name__ == '__main__':
    SIZE = (10, 10)
    WINDOW_SIZE = (500, 500)
    environment = Environment(SIZE)
    display = DisplayEnvironment(WINDOW_SIZE, SIZE)

    RUN = True
    while RUN:
        for event in pg.event.get():
            if event.type == QUIT:
                RUN = False

        display.update(environment.get_data())
