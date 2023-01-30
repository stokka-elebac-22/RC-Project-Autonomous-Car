'''Main'''
import cv2 as cv
import pygame as pg
import math
from pygame.locals import QUIT # pylint: disable=no-name-in-module
from environment.src.environment import Environment
from environment.src.display import DisplayEnvironment
from environment.src.a_star import AStar

# function for line generation
import numpy as np

# https://github.com/encukou/bresenham

def bresenham(x0, y0, x1, y1):
    """Yield integer coordinates on the line from (x0, y0) to (x1, y1).
    Input coordinates should be integers.
    The result will contain both the start and the end point.
    """
    coordinates = []
    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2*dy - dx
    y = 0

    for x in range(dx + 1):
        coordinates.append((x0 + x*xx + y*yx, y0 + x*xy + y*yy))
        if D >= 0:
            y += 1
            D -= 2*dx
        D += 2*dy

    return coordinates


class PathFinding:
    
    def __init__(self, size, w_size, pixel_width, pixel_height, cam_width, cam_height, object_id=10):
        self.ratio_width = pixel_width/cam_width
        self.ratio_height = pixel_height/cam_height
        self.size = size
        self.window_size = (w_size* (size[1]/size[0]), w_size)
        self.display = DisplayEnvironment(self.window_size, size)
        self.env = Environment(size, 30, {'view_point': None, 'object_id': object_id})
    
    def point_to_distance(self, point):
        x_value = point[0]*self.ratio_width
        y_value = point[1]*self.ratio_height
        return (x_value, y_value)

    def calculate_path(self, point, obstacles):
        self.env.remove(12)
        converted_point = self.point_to_distance(point)
        self.env.insert(converted_point, 12)

        for groups in obstacles:
            line = []
            for group in groups:
                ret, coord = self.env.insert(group, 1)
                if coord is not None:
                    line.append(coord[0])
                    line.append(coord[1])
            
            if len(groups) == 2:
                result = bresenham(line[0], line[1], line[2], line[3])
                if result is not None:
                    for pt in result:
                        self.env.insert_by_index(pt, 1)

        start_pos_path = self.env.get_pos(10)
        end_pos_path = self.env.get_pos(11)

        cur_mat = self.env.get_data()
        self.display.update(cur_mat)
        cur_mat = self.env.get_data()
        ret, path = AStar().get_data(cur_mat, start_pos_path, end_pos_path)

        if ret:
            for pos in path[1:-1]:
                self.display.insert(pos, 'Path')

        self.display.display()


if __name__ == "__main__":
    PIXEL_WIDTH = 500
    PIXEL_HEIGHT = 300
    CAM_WIDTH = 1000
    CAM_HEIGHT = 500
    path_finding = PathFinding((30, 51), 600, PIXEL_WIDTH, PIXEL_HEIGHT, CAM_WIDTH, CAM_HEIGHT)
    RUN = True
    while RUN:
        for event in pg.event.get():
            if event.type == QUIT:
                RUN = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                TILE_SIZE = path_finding.window_size[1]/path_finding.size[0]
                col = mouse_pos[0] // TILE_SIZE
                row = mouse_pos[1] // TILE_SIZE
                path_finding.env.insert_by_index((int(row), int(col)), '1')

        path_finding.calculate_path((3,3), [[(100, 200), (200,500)], [(-200, 300)]])