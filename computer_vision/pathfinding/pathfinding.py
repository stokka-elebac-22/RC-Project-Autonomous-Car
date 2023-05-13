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
    from environment.src.a_star import AStar
except ImportError:
    from computer_vision.environment.src.environment import Environment
    from computer_vision.environment.src.a_star import AStar


class PathFinding:
    '''
    Class using 2D environmentironment mapping to calculate shortest
    path with objects that can be hindrances
    '''

    def __init__(self,
                 environment: Environment,
                 pathfinding_algorithm: AStar,
                 tension: float = 0.,
                 velocity: float = 10,
                 num_points: int = 3,
                 rotate_time: float = 0.1):  # pylint: disable=R0913
        self.tension = tension
        self.velocity = velocity
        self.num_points = num_points
        self.__environment = environment
        self.__pathfinding_algorithm = pathfinding_algorithm
        self.rotate_time = rotate_time

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
        self.__environment.insert_objects(objects)

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
            if previous_angle - tol <= angles[i+1] <= previous_angle + tol \
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

    def catmull_t_j(self, t_i, p_i, p_j, alpha):
        '''Method to calculate t_p'''
        x_i, y_i = p_i
        x_j, y_j = p_j
        return (((x_j-x_i)**2+(y_j-y_i)**2)**0.5)**alpha + t_i

    def catmull_rom_segment(self, p_0, p_1, p_2, p_3, alpha, num_points=100):  # pylint: disable=R0913 R0914
        '''
        p_0, p_1, p_2, and p_3: (x, y) pairs
        num_points: number of points in the segment
        '''
        p_0, p_1, p_2, p_3 = map(np.array, [p_0, p_1, p_2, p_3])

        t_0 = 0
        t_1 = self.catmull_t_j(t_0, p_0, p_1, alpha)
        t_2 = self.catmull_t_j(t_1, p_1, p_2, alpha)
        t_3 = self.catmull_t_j(t_2, p_2, p_3, alpha)

        t_p = np.linspace(t_1, t_2, num_points)
        t_p = t_p.reshape(len(t_p), 1)

        a_1 = (t_1-t_p)/(t_1-t_0)*p_0+(t_p-t_0)/(t_1-t_0)*p_1
        a_2 = (t_2-t_p)/(t_2-t_1)*p_1+(t_p-t_1)/(t_2-t_1)*p_2
        a_3 = (t_3-t_p)/(t_3-t_2)*p_2+(t_p-t_2)/(t_3-t_2)*p_3

        b_1 = (t_2-t_p)/(t_2-t_0)*a_1+(t_p-t_0)/(t_2-t_0)*a_2
        b_2 = (t_3-t_p)/(t_3-t_1)*a_2+(t_p-t_1)/(t_3-t_1)*a_3

        c_o = (t_2-t_p)/(t_2-t_1)*b_1+(t_p-t_1)/(t_2-t_1)*b_2

        a1_d = (p_1-p_0)/(t_1-t_0)
        a2_d = (p_2-p_1)/(t_2-t_1)
        a3_d = (p_3-p_2)/(t_3-t_2)

        b1_d = (a_2-a_1)/(t_2-t_0)+(t_2-t_p) / \
            (t_2-t_0)*a1_d+(t_p-t_0)/(t_2-t_0)*a2_d
        b2_d = (a_3-a_2)/(t_3-t_1)+(t_3-t_p) / \
            (t_3-t_1)*a2_d+(t_p-t_1)/(t_3-t_1)*a3_d

        c_d = (b_2-b_1)/(t_2-t_1)+(t_2-t_p) / \
            (t_2-t_1)*b1_d+(t_p-t_1)/(t_2-t_1)*b2_d
        return c_o, c_d

    def catmull_rom_spline(self, points, alpha, num_points=100):
        '''
        Calculate Catmull Rom spline for a list of points
        and return the points on the spline and the derivative
        '''
        # c: points on the curve
        # v: derivative of the curve
        curve = []
        derivative = []
        for i in range(len(points)-3):
            c_value, d_value = self.catmull_rom_segment(
                points[i], points[i+1], points[i +
                                               2], points[i+3], alpha, num_points
            )
            curve.extend(c_value)
            derivative.extend(d_value)

        return curve, derivative

    def approx_segment_lengths(self, points):
        '''Approximate the length of a segment (between two points)'''
        lengths = []
        prev_point = None

        for point in points:
            if prev_point is None:
                prev_point = point
                continue
            curr_point = point
            lengths.append(
                math.sqrt((curr_point[0]-prev_point[0])**2+(curr_point[1]-prev_point[1])**2))
            prev_point = curr_point

        return lengths

    def get_angle_diff(self, angles: float) -> list[list[np.ndarray], list[np.ndarray]]:
        '''Calculate the change in angle'''
        current_ang = 0
        angle_diff = []
        for next_ang in angles:
            first_diff = math.dist([current_ang], [next_ang])
            second_diff = 360-abs(first_diff)
            minimum_diff = min(abs(first_diff), second_diff)
            if current_ang > next_ang:
                if abs(first_diff) == minimum_diff:
                    minimum_diff = minimum_diff*-1
            else:
                if abs(second_diff) == minimum_diff:
                    minimum_diff = minimum_diff*-1
            angle_diff.append(minimum_diff)
            current_ang = next_ang
        return angle_diff

    def get_angle(self, point_one: tuple, point_two: tuple):
        '''Get the angle from -180 to 180 where y-axis is 0'''
        x_val = point_two[0] - point_one[0]
        y_val = point_two[1] - point_one[1]
        if x_val == 0:
            return 0
        rad = math.atan(y_val/x_val)
        degrees = math.degrees(rad)

        if x_val > 0:
            degrees = 90 + degrees
        else:
            degrees = -90 + degrees
        return degrees

    # pylint: disable=R0914

    def calculate_path(self, start_object: int, end_object: int) -> dict:
        '''
        Calculate the shortest path from a
        specific object to another object using AStar algorithm
        '''

        start_pos_path = self.__environment.get_pos(start_object)
        end_pos_path = self.__environment.get_pos(end_object)

        cur_mat = self.__environment.get_data()
        _, path = self.__pathfinding_algorithm.get_data(
            cur_mat, start_pos_path, end_pos_path)

        if path:
            temp_path = [(value[1], value[0])
                        for _, value in enumerate(path)]
            temp_path.reverse()
            curve, _ = self.catmull_rom_spline(
                temp_path, self.tension, self.num_points)
            lengths = self.approx_segment_lengths(curve)
            distances = [x * self.__environment.real_size for x in lengths]
            times = [ x / self.velocity for x in distances]

            angles = []
            for i, value in enumerate(curve):
                if i != 0:
                    angles.append(self.get_angle(curve[i-1], value))

            data = self.merge_similar_angles(times[:-1], angles[:-1], 1)
            data['angles'].append(angles[-1])
            angle_diff = self.get_angle_diff(data['angles'])
            if not angle_diff:
                return None
            data['times'] = [self.rotate_time*angle_diff[0]] + data['times']
            return {
                'path': path,
                'curve': curve,
                'angles': angle_diff,
                'times': data['times'],
                'distances': distances
            }
        return None
