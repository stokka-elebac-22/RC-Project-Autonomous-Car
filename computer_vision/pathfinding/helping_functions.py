import math

def get_angle(v):
    rad_result = math.atan(v[1]/v[0])
    degrees_result = math.degrees(rad_result)
    if v[1] < 0 and v[0] > 0:
        degrees_result += 180
    elif v[1] < 0 and v[0] < 0:
        degrees_result -= 180
    return degrees_result

def get_abs_velo(v):
    return math.sqrt(v[0]**2 + v[1]**2)