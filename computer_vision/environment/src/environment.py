'''Environment'''
from typing import TypedDict, Tuple
import copy
import numpy as np
from computer_vision.pathfinding.bresenham import bresenham

ViewPointObject = TypedDict('ViewPointObject', {
    'view_point': Tuple[int, int],
    'object_id': int,
})

Objects = TypedDict('Objects', {
    'values': list[tuple],
    'distance': bool,
    'object_id': int
})


class Environment:
    '''Creating a 2 dimensional map of the 3 dimensional world'''

    def __init__(self, size: Tuple[int, int], pixel_size: Tuple[int, int], real_size: float,
                 view_point_object: ViewPointObject = None):
        '''View point is the position in a 2d matrix where everyting should be relativ too'''
        self.size = size
        self.real_size = real_size  # the real unit size per square
        self.pixel_size = pixel_size
        self.map = np.zeros(self.size)

        self.view_point = (self.size[0]-1, self.size[1]//2)
        self.view_point_object = view_point_object
        self.__init_object()

    def __init_object(self) -> None:
        '''Init object'''
        object_id = 0
        if self.view_point_object is not None:
            if self.view_point_object.get('view_point') is not None:
                self.view_point = self.view_point_object.get('view_point')
            if self.view_point_object.get('object_id') is not None:
                object_id = self.view_point_object.get('object_id')
        self.map[self.view_point[0]][self.view_point[1]] = object_id

    def update(self) -> None:
        '''Update the map'''

    def reset(self):
        '''Reset the map'''
        self.map = np.zeros(self.size)
        self.__init_object()

    def get_data(self) -> np.ndarray:
        '''
        Returns the data
        map: the matrix
        '''
        # needs do send a copy of the map, else it will get modified
        return copy.deepcopy(self.map)

    def get_pos(self, object_id: int) -> Tuple[int, int]:
        '''Find the position of the tile with corresponding id'''
        for i, row in enumerate(self.map):
            for j, col in enumerate(row):
                if col == object_id:
                    return (i, j)
        return None

    # pylint: disable=E1136
    def point_to_distance(self, point: tuple[int, int]) -> tuple[float, float]:
        '''Converts point to distance'''
        offset_x = point[0] - self.pixel_size[0]/2
        offset_y = self.pixel_size[1] - point[1]
        # Height 123mm
        y_distance = -0.000000443*pow(np.int64(offset_y), np.int64(4)) \
            + 0.0002751831*pow(np.int64(offset_y), np.int64(3)) \
            - 0.0382433809*pow(np.int64(offset_y), np.int64(2)) \
            + 3.0818720986*offset_y \
            + 341.0336777149
        ratio_x = 0.0008436826 * y_distance - 0.0171120596
        if y_distance > 1700:
            y_distance = 1700
        x_distance = offset_x*ratio_x
        return (x_distance, y_distance)

    def insert(self, distance: Tuple[float, float], object_id: int) -> bool:
        '''
        Insert object
        The distance contains a x and y value (direction)
        '''
        if distance[1] < 0:
            # distance in y direction needs to be positive
            return False, None
        if distance[1] == 0:
            # so it does not collide with view point
            row = self.view_point[0]-1
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

    def remove(self, object_id: int, remove_all: bool = False):
        '''Remove an object'''
        for i, row in enumerate(self.map):
            for j, col in enumerate(row):
                if col == object_id:
                    self.map[i][j] = 0
                    if remove_all:
                        continue
                    return

    def insert_by_index(self, pos: Tuple[int, int], object_id: int):
        '''Insert object by index'''
        if pos[0] < 0 or pos[0] >= self.size[0] or pos[1] < 0 or pos[1] > self.size[1]:
            return False
        self.map[pos[0]][pos[1]] = object_id
        return True

    def insert_objects(self, objects: list[Objects]) -> None:
        '''Insert objects into environment'''
        for groups in objects:
            coords = []
            if groups['values'] is not None:
                for group in groups['values']:
                    if groups['distance']:
                        _, coord = self.insert(group, groups['object_id'])
                    else:
                        distance = self.point_to_distance(group)
                        _, coord = self.insert(
                            distance, groups['object_id'])
                    if coord is not None:
                        coords.append(coord[0])
                        coords.append(coord[1])

                if len(coords) == 4:
                    result = bresenham(
                        (coords[0], coords[1]), (coords[2], coords[3]))
                    if result is not None:
                        for point in result:
                            self.insert_by_index(point, groups['object_id'])
