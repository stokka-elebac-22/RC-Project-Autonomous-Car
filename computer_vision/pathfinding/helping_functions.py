import math

def get_angle(v):
    '''Get the angle from -180 to 180 where y-axis is 0'''
    rad_result = math.atan(v[1]/v[0])
    degrees_result = math.degrees(rad_result)
    if v[1] < 0 and v[0] > 0:
        degrees_result += 180
    elif v[1] < 0 and v[0] < 0:
        degrees_result -= 180
    return degrees_result

def get_abs_velo(v):
    """Calculate the absolute value of a vector"""
    return math.sqrt(v[0]**2 + v[1]**2)