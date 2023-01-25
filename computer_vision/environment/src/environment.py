'''Environment'''
import numpy as np

class Environment:
    '''Creating a 2 dimensional map of the 3 dimensional world'''
    def __init__(self, size, real_size):
        self.size = size
        self.real_size = real_size # the real unit size per square
        self.map = np.zeros(size)

    def update(self):
        '''Update the map'''

    def get_data(self):
        '''
        Returns the data
        map: the matrix
        '''
        return self.map

    def insert_object(self, distance_x, distance_y, object_id):
        '''Insert object'''
        if distance_x == 0:
            row = -1
        else:
            row = -self.size[0]*self.real_size//distance_x
        if distance_y == 0:
            col = -1
        else:
            col = -(self.size[1]*self.real_size/2)//distance_y
        self.map[row][col] = object_id
        print(self.map)
