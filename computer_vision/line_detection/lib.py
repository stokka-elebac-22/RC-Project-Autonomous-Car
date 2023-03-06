'''Importing libraries'''
import math
import numpy as np
np.seterr(all='raise')

class MergeLines():
    '''Merge close lines together'''
    def __init__(self, d_max_xg = 200, d_max_yg = None):
        '''Init'''
        self.d_max_xg = d_max_xg
        if d_max_yg is None:
            d_max_yg = [30, 30, 30]
        self.d_max_yg = d_max_yg

    def length(self, x_1, y_1, x_2, y_2):
        '''Calculate length of a line'''
        return math.sqrt((x_1-x_2)**2+(y_1-y_2)**2)

    def centroid(self, p_a, p_b, p_c, p_d):
        '''
        Calculate centroid of two lines defined by
        Line one: a, b
        Line two: c, d
        '''
        l_i = self.length(p_a[0], p_a[1], p_b[0], p_b[1])
        l_j = self.length(p_c[0], p_c[1], p_d[0], p_d[1])
        x_g = (l_i*(p_a[0]+p_b[0])+l_j*(p_c[0]+p_d[0]))/(2*(l_i+l_j))
        y_g = (l_i*(p_a[1]+p_b[1])+l_j*(p_c[1]+p_d[1]))/(2*(l_i+l_j))
        return (x_g, y_g)

    def orientation(self, p_a, p_b):
        '''Calculate the orientation of a line represented from two points between 0 and PI'''
        angle = math.atan2(abs((p_a[1] - p_b[1])), abs((p_a[0] - p_b[0])))
        if p_a[0] > p_b[0]:
            diff = p_a[1]-p_b[1]
        else:
            diff = p_b[1]-p_a[1]
        if diff < 0:
            angle = math.pi-angle
        return angle

    def merged_line_orientation(self, p_a, p_b, p_c, p_d):
        '''Merged line orientation'''
        orientation_i = self.orientation(p_a, p_b)
        orientation_j = self.orientation(p_c, p_d)
        l_i = self.length(p_a[0], p_a[1], p_b[0], p_b[1])
        l_j = self.length(p_c[0], p_c[1], p_d[0], p_d[1])

        if abs(orientation_i-orientation_j) <= math.pi/2:
            orientation_r = (l_i*orientation_i + l_j*orientation_j)/(l_i + l_j)
        else:
            orientation_r = (l_i*orientation_i + l_j*(orientation_j
                        - math.pi*orientation_j/abs(orientation_j)))/(l_i + l_j)
        return orientation_r

    def transform_to_another_axis(self, centroid, point, orientation):
        '''
        Transform the given point to a new axis
        centered on the centroid with the given orientation
        '''
        new_x = (point[1]-centroid[1])*math.sin(orientation) \
                + (point[0]-centroid[0])*math.cos(orientation)
        new_y = (point[1]-centroid[1])*math.cos(orientation) \
                - (point[0]-centroid[0])*math.sin(orientation)
        return (new_x, new_y)

    def transform_to_orig_axis(self, centroid, point, orientation):
        '''Transform the given point to original axis'''
        try:
            orig_x = (((point[0]+centroid[1]*math.sin(orientation)
                        +centroid[0]*math.cos(orientation))
                       /math.sin(orientation))*math.cos(orientation)
                       -centroid[1]*math.cos(orientation)+centroid[0]
                       *math.sin(orientation)-point[1])/(math.cos(orientation)**2/
                       math.sin(orientation)+math.sin(orientation))
            orig_y = (point[0]+centroid[1]*math.sin(orientation)-orig_x*
                      math.cos(orientation)+centroid[0]*math.cos(orientation))/math.sin(orientation)
        except ZeroDivisionError:
            orig_x = point[0]+centroid[0]
            orig_y = point[1]+centroid[1]
        except FloatingPointError:
            orig_x = point[0]+centroid[0]
            orig_y = point[1]+centroid[1]
        return (int(round(orig_x))), int(round(orig_y))

    def merge_lines(self, p_a, p_b, p_c, p_d):
        '''
        Merge two lines
        line one: (p_a, p_b)
        line two: (p_c, p_d)
        '''
        orientation_i = self.orientation(p_a, p_b)
        orientation_j = self.orientation(p_c, p_d)

        if abs(orientation_i-orientation_j) > math.pi/8:
            return None

        centroid = self.centroid(p_a, p_b, p_c, p_d)
        orientation_r = self.merged_line_orientation(p_a, p_b, p_c, p_d)
        new_p_a = self.transform_to_another_axis(centroid, p_a, orientation_r)
        new_p_b = self.transform_to_another_axis(centroid, p_b, orientation_r)
        new_p_c = self.transform_to_another_axis(centroid, p_c, orientation_r)
        new_p_d = self.transform_to_another_axis(centroid, p_d, orientation_r)
        new_points = [new_p_a, new_p_b, new_p_c, new_p_d]

        new_x = [p[0] for p in new_points]
        max_x_value = max(new_x)
        max_x_index = new_x.index(max_x_value)
        min_x_value = min(new_x)
        min_x_index = new_x.index(min_x_value)

        l_r = max_x_value - min_x_value
        start_x = (new_points[max_x_index][0], 0)
        stop_x = (new_points[min_x_index][0], 0)

        new_y_line_one = [p[1] for p in new_points[0:2]]
        new_y_line_two = [p[1] for p in new_points[2:4]]

        line_one_index = 0
        line_two_index = 0
        diff = 0

        for i, a_value in enumerate(new_y_line_one):
            for j, b_value in enumerate(new_y_line_two):
                if abs(a_value-b_value) > diff:
                    line_one_index = i
                    line_two_index = j + 2
                    diff = abs(a_value-b_value)

        if new_points[line_one_index][1] > new_points[line_two_index][1]:
            min_y_index = line_two_index
            max_y_index = line_one_index
        else:
            max_y_index = line_two_index
            min_y_index = line_one_index

        m_p_one = self.transform_to_orig_axis(centroid, start_x, orientation_r)
        m_p_two = self.transform_to_orig_axis(centroid, stop_x, orientation_r)

        # Case 1
        if abs(l_r) >= (abs(new_p_a[0]-new_p_b[0])+abs(new_p_c[0]-new_p_d[0])):
            if abs(l_r) - (abs(new_p_a[0]-new_p_b[0]) + abs(new_p_c[0]-new_p_d[0])) \
            <= self.d_max_xg and abs(new_points[max_y_index][1]-new_points[min_y_index][1]) \
            <= self.d_max_yg[0]:
                return np.array([m_p_one[0], m_p_one[1], m_p_two[0], m_p_two[1]])
        # Case 2
        elif abs(l_r) == abs(new_p_a[0]-new_p_b[0]) or abs(l_r) == abs(new_p_c[0]-new_p_d[0]):
            if abs(new_points[max_y_index][1]-new_points[min_y_index][1]) <= self.d_max_yg[1]:
                return np.array([m_p_one[0], m_p_one[1], m_p_two[0], m_p_two[1]])
        # Case 3
        elif abs(l_r) < (abs(new_p_a[0]-new_p_b[0])+abs(new_p_c[0]-new_p_d[0])):
            if abs(new_points[max_y_index][1]-new_points[min_y_index][1]) <= self.d_max_yg[2]:
                return np.array([m_p_one[0], m_p_one[1], m_p_two[0], m_p_two[1]])
        return None

    def merge_all_lines(self, lines):
        '''Merge all lines'''
        merged_index = []
        merged_lines = []
        for a_index, i in enumerate(lines):
            if a_index in merged_index:
                continue
            merged_index.append(a_index)
            current_line = i
            for b_index, j in enumerate(lines):
                if b_index in merged_index:
                    continue
                new_merged_line = self.merge_lines((current_line[0], current_line[1]),
                (current_line[2], current_line[3]), (j[0], j[1]), (j[2], j[3]))
                if new_merged_line is not None:
                    current_line = new_merged_line
                    merged_index.append(b_index)
            merged_lines.append(current_line)

        return merged_lines
