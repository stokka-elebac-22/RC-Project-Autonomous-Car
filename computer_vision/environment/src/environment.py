'''Environment'''
import numpy as np

class Environment:
    '''Creating a 2 dimensional map of the 3 dimensional world'''
    def __init__(self, size):
        self.size = size
        self.map = np.zeros(size)

    def update(self):
        '''Update the map'''

    def get_data(self):
        '''
        Returns the data
        map: the matrix
        '''
