'''Importing libraries'''
import math
import numpy as np
from environment.src.display import DisplayEnvironment
from environment.src.environment import Environment

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

def get_angle_diff(angles: float) -> list[list[np.ndarray], list[np.ndarray]]:
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
