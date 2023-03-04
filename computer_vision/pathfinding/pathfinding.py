'''Main'''
import os
import sys
import math
from typing import TypedDict
import numpy as np
try:
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)
    from environment.src.environment import Environment
    from environment.src.display import DisplayEnvironment
    from environment.src.a_star import AStar
    from bresenham import bresenham
    from spline import catmull_rom_chain, approx_segment_lengths
    from lib import get_abs_velo, get_angle, get_angle_diff
except ImportError:
    from computer_vision.environment.src.environment import Environment
    from computer_vision.environment.src.display import DisplayEnvironment
    from computer_vision.environment.src.a_star import AStar
    from computer_vision.pathfinding.bresenham import bresenham
    from computer_vision.pathfinding.spline import catmull_rom_chain, approx_segment_lengths
    from computer_vision.pathfinding.lib import get_abs_velo, get_angle, get_angle_diff

class PathFinding:
    '''
    Class using 2D environment mapping to calculate shortest
    path with objects that can be hindrances
    '''
    def __init__(self, size: tuple[int, int], pixel_width:int, pixel_height:int,
                object_id:int=10, tension:float=0., velocity:float = 10, display:DisplayEnvironment=None, env_size:int = 20
                ): # pylint: disable=R0913
        self.pixel_width = pixel_width 
        self.pixel_height = pixel_height
        self.size = size
        self.display = display
        self.tension = tension
        self.velocity = velocity
        self.env = Environment(
            size, env_size, {'view_point': None, 'object_id': object_id})
        self.center = (pixel_width, pixel_height)
        self.a_star = AStar(weight=2, penalty=100)

    def point_to_distance(self, point:tuple[int, int]) -> tuple[float, float]:
        '''Converts point to distance'''
        offset_x = point[0] - self.center[0]/2
        offset_y = self.pixel_width - point[1]
        # Added 150 offset
        y_distance = 0.0000005405*pow(np.int64(offset_y), np.int64(4))-0.0002915424*pow(np.int64(offset_y), np.int64(3))+0.0579638581*pow(np.int64(offset_y), np.int64(2))-2.4604486471*offset_y+430.4886090479 - 150
        ratio_x= 0.0008111433472 * y_distance - 0.0096054187869
        if y_distance > 2500:
            y_distance=2500
        x_distance = offset_x*ratio_x
        return (x_distance, y_distance)

    # TODO: Maybe fix later
    def distance_to_point(self, distance:tuple[float, float]) -> tuple[int, int]:
        '''Converts distance to point'''
        # x_0 = 5.405*10**(-7)*pow(np.int64(self.pixel_height), np.int64(4)) - 0.0002915424*pow(np.int64(self.pixel_height), np.int64(3))+0.0579638581*pow(np.int64(self.pixel_height), np.int64(2))-2.4604486471*self.pixel_height+430.4886090479-150
        # x_1 = -0.00002162*pow(np.int64(self.pixel_height), np.int64(3))+0.0008746272*pow(np.int64(self.pixel_height), np.int64(2))-0.1159277162*self.pixel_height+2.4604486471
        # x_2 = 0.000003243*pow(np.int64(self.pixel_height), np.int64(2))-0.0008746272*self.pixel_width+0.0579638581
        # x_3 = -0.000002162*self.pixel_width+0.0002915424
        # x_4 = 5.405*10**(-7)
        p_x = math.floor((distance[0]/1) + self.center[0]/1)
        p_y = math.floor(self.center[1] - (distance[1]/1))
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
                        (coords[0], coords[1]), (coords[2], coords[3]))
                    if result is not None:
                        for point in result:
                            self.env.insert_by_index(point, groups['object_id'])


    def calculate_path(self, value: tuple[int, int], distance: bool) -> list[tuple]:
        '''Calculate the shortest path to a specific point using AStar algorithm'''
        self.env.remove(3)
        if not distance:
            point = self.point_to_distance(value)
        else:
            point = value
        self.env.insert(point, 3)

        start_pos_path = self.env.get_pos(10)
        end_pos_path = self.env.get_pos(3)

        cur_mat = self.env.get_data()
        _, path = self.a_star.get_data(cur_mat, start_pos_path, end_pos_path)

        if path:
            new_path = [(value[1], value[0])
                        for i, value in enumerate(path) if i % 3 == 0]
            temp_path = [(path[0][1], path[0][0])]
            temp_path = temp_path + new_path
            for _ in range(2):
                temp_path.append((path[len(path) - 1][1], path[len(path) - 1][0]))

            temp_path.reverse()
            c, v = catmull_rom_chain(temp_path, self.tension)
            lengths = approx_segment_lengths(c)
            times = [x / self.velocity for x in lengths]

            # TODO: muligens trenge ikke abs velo
            # ENDRE VELOCITYCONSTANT Eller numpoints i catmull spline
            abs_velos = []
            angles = []
            for value in v:
                abs_velos.append(get_abs_velo(value))
                angles.append(get_angle(value))

            angle_diff = get_angle_diff(angles)

            return {
                'path': path,
                'curve': c,
                'angles': angle_diff,
                'times': times,
            }
        return None

    def update_display(self, path):
        '''Update display if there are new changes'''
        if self.display is not None:
            cur_mat = self.env.get_data()
            self.display.update(cur_mat)
            if path:
                for pos in path[1:-1]:
                    self.display.insert(pos, 'Path')