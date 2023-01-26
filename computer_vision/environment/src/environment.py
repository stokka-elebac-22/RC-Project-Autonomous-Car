'''Environment'''
import copy
import numpy as np

class Environment:
    '''Creating a 2 dimensional map of the 3 dimensional world'''
    def __init__(self, size, real_size):
        self.size = size
        self.real_size = real_size # the real unit size per square
        self.__map = np.zeros(size)

    def update(self):
        '''Update the map'''

    def get_data(self):
        '''
        Returns the data
        map: the matrix
        '''
        # needs do send a copy of the map, else it will get modified
        return copy.copy(self.__map)

    def insert_object(self, distance_x, distance_y, object_id):
        '''Insert object'''
        if distance_y == 0:
            row = self.size[1]//2
        else:
            row = (self.size[1]*self.real_size/2)//distance_y
        if distance_x == 0:
            col = self.size[0]//2
        else:
            col = self.size[0]*self.real_size//distance_x
        self.__map[int(row)][int(col)] = object_id
