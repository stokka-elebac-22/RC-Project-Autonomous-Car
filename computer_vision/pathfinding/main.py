'''Main'''
import os
import sys
import math
from typing import TypedDict
try:
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)
    from environment.src.environment import Environment
    from environment.src.display import DisplayEnvironment
    from environment.src.a_star import AStar
    from bresenham import bresenham
except ImportError:
    from computer_vision.environment.src.environment import Environment
    from computer_vision.environment.src.display import DisplayEnvironment
    from computer_vision.environment.src.a_star import AStar


class PathFinding:
    '''
    Class using 2D environment mapping to calculate shortest
    path with objects that can be hindrances
    '''
    def __init__(self, size: tuple[int, int], pixel_width:int, pixel_height:int
                ,cam_width:int, cam_height:int, cam_center:list[int, int],
                object_id:int=10, display:DisplayEnvironment=None, env_size:int = 20
                ):
        self.ratio_width = cam_width/pixel_width
        self.ratio_height = cam_height/pixel_height
        self.size = size
        self.display = display
        self.env = Environment(
            size, env_size, {'view_point': None, 'object_id': object_id})
        self.center = cam_center
        self.a_star = AStar(weight=2, penalty=100)

    def point_to_distance(self, point:tuple[int, int]) -> tuple[float, float]:
        '''Converts point to distance'''
        offset_x = point[0] - self.center[0]/2
        offset_y = self.center[1] - point[1]
        x_distance = offset_x*self.ratio_width
        y_distance = offset_y*self.ratio_height
        return (x_distance, y_distance)

    def distance_to_point(self, distance:tuple[float, float]) -> tuple[int, int]:
        '''Converts distance to point'''
        p_x = math.floor((distance[0]/self.ratio_width) + self.center[0]/2)
        p_y = math.floor(self.center[1] - (distance[1]/self.ratio_height))
        return (p_x, p_y)

    Objects = TypedDict('Objects', {
        'points': list[tuple[int, int]],
        'distances': list[tuple[int, int]],
        'object_id': int
    })
    def insert_objects(self, objects: Objects) -> None:
        '''Insert objects into environment'''
        for groups in objects:
            coords = []
            if groups['values'] is not None:
                for group in groups['values']:
                    if groups['distance']:
                        _, coord = self.env.insert(group, groups['object_id'])
                    else:
                        distance = self.point_to_distance(group)
                        _, coord = self.env.insert(
                            distance, groups['object_id'])
                    if coord is not None:
                        coords.append(coord[0])
                        coords.append(coord[1])

                if len(coords) == 4:
                    result = bresenham(
                        coords[0], coords[1], coords[2], coords[3])
                    if result is not None:
                        for point in result:
                            self.env.insert_by_index(point, 1)


    def calculate_path(self, value: tuple[int, int], distance: bool) -> list[tuple]:
        '''Calculate the shortest path to a specific point using AStar algorithm'''
        self.env.remove(12)
        if not distance:
            point = self.point_to_distance(value)
        else:
            point = value
        self.env.insert(point, 12)

        start_pos_path = self.env.get_pos(10)
        end_pos_path = self.env.get_pos(12)

        cur_mat = self.env.get_data()
        _, path = self.a_star.get_data(cur_mat, start_pos_path, end_pos_path)
        return path

    def update_display(self, path):
        '''Update display if there are new changes'''
        if self.display is not None:
            cur_mat = self.env.get_data()
            self.display.update(cur_mat)
            for pos in path[1:-1]:
                self.display.insert(pos, 'Path')
