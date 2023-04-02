'''Main'''
import os
import sys
import math
from typing import TypedDict, Tuple
import numpy as np
try:
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)
    from environment.src.environment import Environment
    from environment.src.a_star import AStar
    from bresenham import bresenham
    from spline import catmull_rom_chain, approx_segment_lengths
    from lib import get_angle, get_angle_diff
except ImportError:
    from computer_vision.environment.src.environment import Environment
    from computer_vision.environment.src.a_star import AStar
    from computer_vision.pathfinding.bresenham import bresenham
    from computer_vision.pathfinding.spline import catmull_rom_chain, approx_segment_lengths
    from computer_vision.pathfinding.lib import get_abs_velo, get_angle, get_angle_diff

class PathFinding:
    '''
    Class using 2D environmentironment mapping to calculate shortest
    path with objects that can be hindrances
    '''
    def __init__(self,
                pixel_size: Tuple[int, int],
                environment: Environment,
                pathfinding_algorithm: AStar,
                tension:float=0.,
                velocity:float = 10,
                num_points:int=3,
                rotate_time:float=0.1): # pylint: disable=R0913
        self.pixel_size = pixel_size
        self.tension = tension
        self.velocity = velocity
        self.num_points = num_points
        self.__environment = environment
        self.__pathfinding_algorithm = pathfinding_algorithm
        self.rotate_time = rotate_time

    def point_to_distance(self, point:tuple[int, int]) -> tuple[float, float]:
        '''Converts point to distance'''
        offset_x = point[0] - self.pixel_size[0]/2
        offset_y = self.pixel_size[1] - point[1]
        # Added 150 offset
        y_distance = 0.0000005405*pow(np.int64(offset_y), np.int64(4)) \
                    -0.0002915424*pow(np.int64(offset_y), np.int64(3)) \
                    +0.0579638581*pow(np.int64(offset_y), np.int64(2)) \
                    -2.4604486471*offset_y+430.4886090479 - 150
        ratio_x= 0.0008111433472 * y_distance - 0.0096054187869
        if y_distance > 2500:
            y_distance=2500
        x_distance = offset_x*ratio_x
        return (x_distance, y_distance)

    # TODO: Maybe fix later
    def distance_to_point(self, distance:tuple[float, float]) -> tuple[int, int]:
        '''Converts distance to point'''
        # x_0 = 5.405*10**(-7)*pow(np.int64(self.pixel_height), np.int64(4)) \
        # - 0.0002915424*pow(np.int64(self.pixel_height), \
        # np.int64(3))+0.0579638581*pow(np.int64(self.pixel_height),\
        # np.int64(2))-2.4604486471*self.pixel_height+430.4886090479-150
        # x_1 = -0.00002162*pow(np.int64(self.pixel_height),\
        # np.int64(3))+0.0008746272*pow(np.int64(self.pixel_height),\
        # np.int64(2))-0.1159277162*self.pixel_height+2.4604486471
        # x_2 = 0.000003243*pow(np.int64(self.pixel_height), \
        # np.int64(2))-0.0008746272*self.pixel_width+0.0579638581
        # x_3 = -0.000002162*self.pixel_width+0.0002915424
        # x_4 = 5.405*10**(-7)
        p_x = math.floor((distance[0]/1) + self.pixel_size[0]/1)
        p_y = math.floor(self.pixel_size[1] - (distance[1]/1))
        return (p_x, p_y)

    Objects = TypedDict('Objects', {
        'values': list[tuple],
        'distance': bool,
        'object_id': int
    })

    def reset(self):
        '''Reset environment'''
        self.__environment.reset()

    def insert_objects(self, objects: list[Objects]) -> None:
        '''Insert objects into environment'''
        for groups in objects:
            coords = []
            if groups['values'] is not None:
                for group in groups['values']:
                    if groups['distance']:
                        _, coord = self.__environment.insert(group, groups['object_id'])
                    else:
                        distance = self.point_to_distance(group)
                        _, coord = self.__environment.insert(
                            distance, groups['object_id'])
                    if coord is not None:
                        coords.append(coord[0])
                        coords.append(coord[1])

                if len(coords) == 4:
                    result = bresenham(
                        (coords[0], coords[1]), (coords[2], coords[3]))
                    if result is not None:
                        for point in result:
                            self.__environment.insert_by_index(point, groups['object_id'])

    def get_environment(self):
        '''Retrieve environment'''
        return self.__environment
    

    def merge_similar_angles(self, times: list[int], angles: list[float], tol: int = 1) -> dict:
        '''Merge similar angles to reduce the list of angles and times'''
        if not angles or not times:
            return None
        new_angles = []
        new_times = []
        previous_angle = angles[0]
        previous_time = times[0]
        for i in range(len(angles)-1):
            if  previous_angle - tol <= angles[i+1] <= previous_angle + tol \
                or \
                previous_angle - tol >= angles[i+1] >= previous_angle + tol:
                previous_angle = (previous_angle + angles[i+1]) / 2
                previous_time += times[i+1]
            else:
                new_times.append(previous_time)
                new_angles.append(previous_angle)
                previous_angle = angles[i+1]
                previous_time = times[i+1]
        new_times.append(previous_time)
        new_angles.append(previous_angle)
        return {
            'times': new_times, 
            'angles': new_angles
        }


    # pylint: disable=R0914
    def calculate_path(self, start_object: int, end_object: int) -> dict:
        '''
        Calculate the shortest path from a
        specific object to another object using AStar algorithm
        '''

        start_pos_path = self.__environment.get_pos(start_object)
        end_pos_path = self.__environment.get_pos(end_object)

        cur_mat = self.__environment.get_data()
        _, path = self.__pathfinding_algorithm.get_data(cur_mat, start_pos_path, end_pos_path)

        if path:
            new_path = [(value[1], value[0])
                        for i, value in enumerate(path)]
            temp_path = [(path[0][1], path[0][0])]
            temp_path = temp_path + new_path
            for _ in range(1):
                temp_path.append((path[len(path) - 1][1], path[len(path) - 1][0]))
            temp_path.reverse()
            curve, _ = catmull_rom_chain(temp_path, self.tension, self.num_points)
            lengths = approx_segment_lengths(curve)
            times = [x * self.__environment.real_size / self.velocity for x in lengths]

            angles = []
            for i, value in enumerate(curve):
                if i!=0:
                    angles.append(get_angle(curve[i-1], value))

            data = self.merge_similar_angles(times[:-1], angles[:-1], 1)
            data['angles'].append(angles[-1])
            angle_diff = get_angle_diff(data['angles'])
            if not angle_diff:
                return None
            data['times'] = [self.rotate_time*angle_diff[0]] + data['times']
            return {
                'path': path,
                'curve': curve,
                'angles': angle_diff,
                'times': data['times'],
            }
        return None
