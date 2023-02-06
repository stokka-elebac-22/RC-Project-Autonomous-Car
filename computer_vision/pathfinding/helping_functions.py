import math

def derivative(P1, P2):
    p_x = P2[0] - P1[0]
    p_y = P2[1] - P1[1]
    return p_y/p_x

def angle(v):
    rad_result = math.atan(v[1]/v[0])
    degrees_result = math.degrees(rad_result)
    if v[1] < 0 and v[0] > 0:
        degrees_result += 180
    elif v[1] < 0 and v[0] < 0:
        degrees_result -= 180
    return degrees_result