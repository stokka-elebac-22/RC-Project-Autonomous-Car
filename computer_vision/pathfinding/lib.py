'''Importing libraries'''
import math
from typing import Tuple
from computer_vision.environment.src.display import DisplayEnvironment
from computer_vision.environment.src.environment import Environment

def get_angle(vec: list) -> float:
    '''Get the angle from -180 to 180 where y-axis is 0'''
    if vec[0] == 0:
        rad_result = 0
    else:
        rad_result = math.atan(vec[1]/vec[0])
    degrees_result = math.degrees(rad_result)
    temp = 90 - degrees_result
    if vec[0] < 0:
        temp =  temp - 180
    if temp == -180:
        temp = 180
    return temp

def get_abs_velo(vec: list) -> float:
    '''Calculate the absolute value of a vector'''
    return math.sqrt(vec[0]**2 + vec[1]**2)

def angle_and_velocity_from_derivative(derivative) -> Tuple[int, int]:
    '''
    This function returns a list of an abs velocity and
    an angle from the curve and the derivative
    '''
    abs_velos = []
    angles = []
    for value in derivative:
        abs_velos.append(get_abs_velo(value))
        angles.append(get_angle(value))
    return abs_velos, angles

def update_display(
          display: DisplayEnvironment,
          environment: Environment,
          path) -> DisplayEnvironment:
    '''Update display if there are new changes'''
    if display is not None:
        cur_mat = environment.get_data()
        display.update(cur_mat)
        for pos in path[1:-1]:
            display.insert(pos, 'Path')
    return display
