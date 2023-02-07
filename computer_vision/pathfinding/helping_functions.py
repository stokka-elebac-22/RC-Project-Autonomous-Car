'''Importing libraries'''
import math

def get_angle(vec: list) -> float:
    '''Get the angle from -180 to 180 where y-axis is 0'''
    rad_result = math.atan(vec[1]/vec[0])
    degrees_result = math.degrees(rad_result)
    if vec[1] < 0 and vec[0] > 0:
        degrees_result += 180
    elif vec[1] < 0 and vec[0] < 0:
        degrees_result -= 180
    return degrees_result

def get_abs_velo(vec: list) -> float:
    """Calculate the absolute value of a vector"""
    return math.sqrt(vec[0]**2 + vec[1]**2)
