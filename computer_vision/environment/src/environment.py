'''Environment'''
from typing import TypedDict
import copy
import numpy as np

ViewPointObject = TypedDict('ViewPointObject', {
    'view_point': tuple[int, int],
    'object_id': int,
})
class Environment:
    '''Creating a 2 dimensional map of the 3 dimensional world'''
    def __init__(self, size: tuple[int, int], real_size: float, view_point_object: ViewPointObject = None):
        '''View point is the position in a 2d matrix where everyting should be relativ too'''
        self.size = size
        self.real_size = real_size # the real unit size per square
        self.map = np.zeros(size)

        self.view_point = (self.size[0]-1, self.size[1]//2)
        object_id = 0

        if view_point_object is not None:
            if view_point_object.get('view_point') is not None:
                self.view_point = view_point_object.get('view_point')
            if view_point_object.get('object_id') is not None:
                object_id = view_point_object.get('object_id')
        self.map[self.view_point[0]][self.view_point[1]] = object_id

    def update(self):
        '''Update the map'''

    def get_data(self):
        '''
        Returns the data
        map: the matrix
        '''
        # needs do send a copy of the map, else it will get modified
        return copy.deepcopy(self.map)

    def get_pos(self, object_id: int):
        '''Find the position of the tile with corresponding id'''
        for i, row in enumerate(self.map):
            for j, col in enumerate(row):
                if col == object_id:
                    return (i, j)
        return None

    def insert(self, distance: tuple[float, float], object_id: int) -> bool:
        '''
        Insert object
        The distance contains a x and y value (direction)
        '''
        if distance[1] < 0:
            # distance in y direction needs to be positive
            return False, None
        if distance[1] == 0:
            row = self.view_point[0]-1 # so it does not collide with view point
        else:
            # Move it up the matrix (down in index), because assuming the viewpoint is upward
            row = self.view_point[0] - distance[1]//self.real_size
        if distance[0] == 0:
            col = self.view_point[1]
        else:
            col = self.view_point[1] + distance[0]//self.real_size
        if row >= self.size[0] or row < 0 or col < 0 or col >= self.size[1]:
            return False, None
        self.map[int(row)][int(col)] = object_id
        return True, (int(row), int(col))

    def remove(self, object_id: int, remove_all: bool=False):
        '''Remove an object'''
        for i, row in enumerate(self.map):
            for j, col in enumerate(row):
                if col == object_id:
                    self.map[i][j] = 0
                    if remove_all:
                        continue
                    return

    def insert_by_index(self, pos: tuple[int, int], object_id: int):
        '''Insert object by index'''
        if pos[0] < 0 or pos[0] >= self.size[0] or pos[1] < 0 or pos[1] > self.size[1]:
            return False
        self.map[pos[0]][pos[1]] = object_id
        return True
