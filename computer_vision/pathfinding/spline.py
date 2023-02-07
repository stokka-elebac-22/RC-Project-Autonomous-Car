'''Import_ing Libraries'''
import numpy as np

# Source: https://stackoverflow.com/quest_ions/1251438/catmull-rom-splines-in-python
# based on formula from wikipedia!!

def t_j(t_i, p_i, p_j, alpha):
    '''Method to calculate t_p'''
    x_i, y_i = p_i
    x_j, y_j = p_j
    return (((x_j-x_i)**2 + (y_j-y_i)**2)**0.5)**alpha + t_i

def catmull_rom_spline(p_0, p_1, p_2, p_3, alpha, num_points=100):
    """
    p_0, p_1, p_2, and p_3: (x, y) pairs
    nPoints: number of points in the segment
    """
    # To do array mult_iplicat_ion convert to numpy array
    p_0, p_1, p_2, p_3 = map(np.array, [p_0, p_1, p_2, p_3])

    # Calculate t_0 to t4
    t_0 = 0
    t_1 = t_j(t_0, p_0, p_1, alpha)
    t_2 = t_j(t_1, p_1, p_2, alpha)
    t_3 = t_j(t_2, p_2, p_3, alpha)

    # Only calculate points between p_1 and p_2
    t_p = np.linspace(t_1, t_2, num_points)

    # Reshape so that we can mult_iply by the points p_0 to p_3
    # and get a point for each value of t_p.
    t_p = t_p.reshape(len(t_p), 1)

    a_1 = (t_1-t_p)/(t_1-t_0)*p_0 + (t_p-t_0)/(t_1-t_0)*p_1
    a_2 = (t_2-t_p)/(t_2-t_1)*p_1 + (t_p-t_1)/(t_2-t_1)*p_2
    a_3 = (t_3-t_p)/(t_3-t_2)*p_2 + (t_p-t_2)/(t_3-t_2)*p_3

    b_1 = (t_2-t_p)/(t_2-t_0)*a_1 + (t_p-t_0)/(t_2-t_0)*a_2
    b_2 = (t_3-t_p)/(t_3-t_1)*a_2 + (t_p-t_1)/(t_3-t_1)*a_3

    c_o = (t_2-t_p)/(t_2-t_1)*b_1 + (t_p-t_1)/(t_2-t_1)*b_2

    a1_d = (p_1-p_0)/(t_1-t_0)
    a2_d = (p_2-p_1)/(t_2-t_1)
    a3_d = (p_3-p_2)/(t_3-t_2)

    b1_d = (a_2-a_1)/(t_2-t_0)+(t_2-t_p)/(t_2-t_0)*a1_d+(t_p-t_0)/(t_2-t_0)*a2_d
    b2_d = (a_3-a_2)/(t_3-t_1)+(t_3-t_p)/(t_3-t_1)*a2_d+(t_p-t_1)/(t_3-t_1)*a3_d

    c_d = (b_2-b_1)/(t_2-t_1)+(t_2-t_p)/(t_2-t_1)*b1_d+(t_p-t_1)/(t_2-t_1)*b2_d
    return c_o, c_d


def catmull_rom_chain(points, alpha):
    """
    Calculate Catmull Rom spline for a list of points
    and return the points on the spline and the derivative
    """
    # c: points on the curve
    # v: derivative of the curve
    curve = []
    derivative = []
    for i in range(len(points)-3):
        c_value, d_value = catmull_rom_spline(
            points[i], points[i+1], points[i+2], points[i+3], alpha
        )
        curve.extend(c_value)
        derivative.extend(d_value)

    return curve, derivative
