'''Main'''
import os
import sys
import math
from typing import TypedDict, Tuple
try:
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)
    from environment.src.environment import Environment
    from environment.src.a_star import AStar
    from bresenham import bresenham
except ImportError:
    from computer_vision.environment.src.environment import Environment
    from computer_vision.environment.src.a_star import AStar

class PathFinding:
    '''
    Class using 2D environmentironment mapping to calculate shortest
    path with objects that can be hindrances
    '''
    # def __init__(self, size: tuple[int, int], pixel_width:int, pixel_height:int
    #             ,cam_width:int, cam_height:int, cam_center:list[int, int],
    #             object_id:int=10, display:Displayenvironmentironment=None, env_size:int = 20
    #             ): # pylint: disable=R0913
    def __init__(self,
                 pixel_size: Tuple[int, int],
                 cam_size: Tuple[int, int],
                 cam_center:list[int, int],
                 environment: Environment,
                 pathfinding_algorithm: AStar):
        '''
        pixel_size contains a width and a height
        cam_size contains a width and a height
        '''
        # object_id:int=10, display:Displayenvironmentironment=None, env_size:int = 20

        self.ratio = {
            'width': cam_size[0]/pixel_size[0],
            'height': cam_size[1]/pixel_size[1]
        }
        # self.display = display
        self.environment = environment
        self.center = cam_center
        self.pathfinding_algorithm = pathfinding_algorithm

    def point_to_distance(self, point:tuple[int, int]) -> tuple[float, float]:
        '''Converts point to distance'''
        offset_x = point[0] - self.center[0]/2
        offset_y = self.center[1] - point[1]
        x_distance = offset_x*self.ratio['width']
        y_distance = offset_y*self.ratio['height']
        return (x_distance, y_distance)

    def distance_to_point(self, distance:tuple[float, float]) -> tuple[int, int]:
        '''Converts distance to point'''
        p_x = math.floor((distance[0]/self.ratio['width']) + self.center[0]/2)
        p_y = math.floor(self.center[1] - (distance[1]/self.ratio['height']))
        return (p_x, p_y)

    Objects = TypedDict('Objects', {
        'points': list[tuple[int, int]],
        'distances': list[tuple[int, int]],
        'object_id': int
    })

    def insert_objects(self, objects: Objects) -> None:
        '''Insert objects into environmentironment'''
        for groups in objects:
            coords = []
            if groups['values'] is not None:
                for group in groups['values']:
                    if groups['distance']:
                        _, coord = self.environment.insert(group, groups['object_id'])
                    else:
                        distance = self.point_to_distance(group)
                        _, coord = self.environment.insert(
                            distance, groups['object_id'])
                    if coord is not None:
                        coords.append(coord[0])
                        coords.append(coord[1])

                if len(coords) == 4:
                    result = bresenham(
                        (coords[0], coords[1]), (coords[2], coords[3]))
                    if result is not None:
                        for point in result:
                            self.environment.insert_by_index(point, 1)


    def calculate_path(self, value: tuple[int, int], distance: bool) -> list[tuple]:
        '''Calculate the shortest path to a specific point using AStar algorithm'''
        self.environment.remove(12)
        if not distance:
            point = self.point_to_distance(value)
        else:
            point = value
        self.environment.insert(point, 12)

        start_pos_path = self.environment.get_pos(10)
        end_pos_path = self.environment.get_pos(12)

        cur_mat = self.environment.get_data()
        _, path = self.pathfinding_algorithm.get_data(cur_mat, start_pos_path, end_pos_path)
        return path
