import numpy as np

# Source: https://stackoverflow.com/questions/1251438/catmull-rom-splines-in-python
# based on formula from wikipedia!!

def tj(ti, Pi, Pj, a):
    xi, yi = Pi
    xj, yj = Pj
    return (((xj-xi)**2 + (yj-yi)**2)**0.5)**a + ti


def CatmullRomDerivative(P0, P1, P2, P3, a, nPoints=100):
    # Convert the points to numpy so that we can do array multiplication
    P0, P1, P2, P3 = map(np.array, [P0, P1, P2, P3])

    # Calculate t0 to t4
    t0 = 0
    t1 = tj(t0, P0, P1, a)
    t2 = tj(t1, P1, P2, a)
    t3 = tj(t2, P2, P3, a)

    # Only calculate points between P1 and P2
    t = np.linspace(t1, t2, nPoints)

    # Reshape so that we can multiply by the points P0 to P3
    # and get a point for each value of t.
    t = t.reshape(len(t), 1)

    A1 = (P1-P0)/(t1-t0)
    A2 = (P2-P1)/(t2-t1)
    A3 = (P3-P2)/(t3-t2)

    B1 = (A2-A1)/(t2-t0)+(t2-t)/(t2-t0)*A1+(t-t0)/(t2-t0)*A2
    B2 = (A3-A2)/(t3-t1)+(t3-t)/(t3-t1)*A2+(t-t1)/(t3-t1)*A3

    C = (B2-B1)/(t2-t1)+(t2-t)/(t2-t1)*B1+(t-t1)/(t2-t1)*B2
    return C


def CatmullRomSpline(P0, P1, P2, P3, a, nPoints=100):
    """
    P0, P1, P2, and P3 should be (x,y) point pairs that define the Catmull-Rom spline.
    nPoints is the number of points to include in this curve segment.
    """
    # Convert the points to numpy so that we can do array multiplication
    P0, P1, P2, P3 = map(np.array, [P0, P1, P2, P3])

    # Calculate t0 to t4
    t0 = 0
    t1 = tj(t0, P0, P1, a)
    t2 = tj(t1, P1, P2, a)
    t3 = tj(t2, P2, P3, a)

    # Only calculate points between P1 and P2
    t = np.linspace(t1, t2, nPoints)

    # Reshape so that we can multiply by the points P0 to P3
    # and get a point for each value of t.
    t = t.reshape(len(t), 1)

    A1 = (t1-t)/(t1-t0)*P0 + (t-t0)/(t1-t0)*P1
    A2 = (t2-t)/(t2-t1)*P1 + (t-t1)/(t2-t1)*P2
    A3 = (t3-t)/(t3-t2)*P2 + (t-t2)/(t3-t2)*P3

    B1 = (t2-t)/(t2-t0)*A1 + (t-t0)/(t2-t0)*A2
    B2 = (t3-t)/(t3-t1)*A2 + (t-t1)/(t3-t1)*A3

    C = (t2-t)/(t2-t1)*B1 + (t-t1)/(t2-t1)*B2

    A1_D = (P1-P0)/(t1-t0)
    A2_D = (P2-P1)/(t2-t1)
    A3_D = (P3-P2)/(t3-t2)

    B1_D = (A2-A1)/(t2-t0)+(t2-t)/(t2-t0)*A1_D+(t-t0)/(t2-t0)*A2_D
    B2_D = (A3-A2)/(t3-t1)+(t3-t)/(t3-t1)*A2_D+(t-t1)/(t3-t1)*A3_D

    C_D = (B2-B1)/(t2-t1)+(t2-t)/(t2-t1)*B1_D+(t-t1)/(t2-t1)*B2_D
    return C, C_D


def CatmullRomChain(P, alpha):
    """
    Calculate Catmull Rom for a chain of points and return the combined curve.
    """
    sz = len(P)

    # The curve C will contain an array of (x,y) points.
    C = []
    V = []
    for i in range(sz-3):
        c, v = CatmullRomSpline(P[i], P[i+1], P[i+2], P[i+3], alpha)
        C.extend(c)
        V.extend(v)

    return C, V
