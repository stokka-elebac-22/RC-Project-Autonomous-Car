'''Library'''
from typing import TypedDict, Tuple
import dataclasses
import math
import pygame as pg

ObjectParam = TypedDict('ObjectParam', {
    'color': pg.Color,
    'thickness': int,
})

@dataclasses.dataclass
class Object:
    '''Object'''
    def __init__(self, object_id: int, name: str, param: ObjectParam):
        self.id = object_id # pylint: disable=C0103
        self.name = name
        self.color = param['color']
        self.thickness = param['thickness']


@dataclasses.dataclass
class Objects:
    '''Class over all the objects'''
    def __init__(self):
        self.objects = TwoWayDict()
        self._init_objects()
        self.object_data = {}
        self._init_object_data()

    def _init_objects(self):
        '''Initializing the object dict'''
        # Choose object id wisely. It should have space to expand if needed,
        # but not exceed 255 (uncesseary use of space)
        obj = [
            # Basic stars at 0
            ('None', 0),
            ('Hindrance', 1),
            ('EndPoint', 2),
            ('Path', 3),
            # Other basic
            ('Car', 10),
            # Parking
            ('QR', 20),
            # Lines
            ('ParkingLine', 30),
            ('LaneLine', 31),
            # Signs
            ('Stop', 40),
        ]
        for i in obj:
            self.objects[i[0]] = i[1]

    def _init_object_data(self):
        '''
        Init object data
        Each object have:
        color, thickness
        '''
        obj = [
            {
                'id': 0,
                'name': 'None',
                'param': {
                    'color': pg.Color(0, 0, 0),
                    'thickness': 1
                }
            },
            {
                'id': 1,
                'name': 'Hindrance',
                'param': {
                    'color': pg.Color(0, 0, 0),
                    'thickness': 0
                }
            },
            {
                'id': 2,
                'name': 'EndPoint',
                'param': {
                    'color': pg.Color(22, 80, 22),
                    'thickness': 0
                }
            },
            {
                'id': 3,
                'name': 'Path',
                'param': {
                    'color': pg.Color(50, 80, 180),
                    'thickness': 0
                }
            },
            {
                'id': 10,
                'name': 'Car',
                'param': {
                    'color': pg.Color(50, 200, 180),
                    'thickness': 0
                }
            },
            {
                'id': 20,
                'name': 'QR',
                'param': {
                    'color': pg.Color(150, 80, 180),
                    'thickness': 0
                }
            },
            {
                'id': 30,
                'name': 'ParkingLine',
                'param': {
                    'color': pg.Color(227,174,87),
                    'thickness': 0
                }
            },
            {
                'id': 31,
                'name': 'LaneLine',
                'param': {
                    'color': pg.Color(204, 204, 150),
                    'thickness': 0
                }
            },
            {
                'id': 40,
                'name': 'Stop',
                'param': {
                    'color': pg.Color(255, 0, 0),
                    'thickness': 0
                }
            },
        ]
        for i in obj:
            new_object = Object(i['id'], i['name'], i['param'])
            self.object_data[i['id']] = new_object

    def get_data(self, obj: Object) -> Object:
        '''
        Get the data of the object
        Each object have:
        color, thickness
        '''
        if not isinstance(obj, (int, float)):
            obj = self.objects.get(obj) # convert to correct keyname
        return self.object_data.get(int(obj))


class TwoWayDict(dict):
    '''
    A two way dict
    src: https://stackoverflow.com/questions/1456373/two-way-reverse-map
    '''
    def __setitem__(self, key, value):
        # Remove any previous connections with these values
        if key in self:
            del self[key]
        if value in self:
            del self[value]
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)

    def __len__(self):
        '''Returns the number of connections'''
        return dict.__len__(self) // 2

NodeData = TypedDict('NodeData', {
    'position': Tuple[int, int],
    'h_value': float,
    'f_value': int,
    'parent': None,
    'weight': int,
    'object_id': int,
})

@dataclasses.dataclass
class Node:
    '''Node'''
    def __init__(self, data: NodeData) -> None:
        self.position = data.get('position')
        if self.position is None:
            self.position = (0,0)
        self.parent: Node = data.get('parent')

        self.object_id: Object = data.get('object_id')
        if self.object_id is None:
            self.object_id = 0

        self.weight = data.get('weight')
        if self.weight is None:
            self.weight = 0

        self.g_value = data.get('g_value')
        if self.g_value is None:
            self.g_value = 0

        self.h_value = data.get('h_value')

        if self.parent is not None:
            self.g_value = self.parent.g_value + math.sqrt(
                abs(self.parent.position[0]-self.position[0])**2 +
                abs(self.parent.position[1]-self.position[1]))

        self.f_value = data.get('f_value')
        if self.h_value is not None and self.weight is not None and self.g_value is not None:
            self.f_value = self.g_value + self.h_value + self.weight
        elif self.f_value is None:
            self.f_value = 0

    def update(self):
        '''Update the node'''
        self.g_value = 0
        if self.parent is not None:
            self.g_value = self.parent.g_value + math.sqrt(
                abs(self.parent.position[0]-self.position[0])**2 +
                abs(self.parent.position[1]-self.position[1]))
        self.f_value = self.g_value + self.h_value + self.weight

    def __eq__(self, other):
        return self.position == other.position


class BinarySearchList:
    '''
    This is a binary search class (just because I could not find a library
    that contained this type of list where you could sort by a key from another class
    '''
    def __init__(self):
        self.__items = []

    def __binary_search(self, value: Node):
        '''
        Binary Search
        https://www.geeksforgeeks.org/python-program-for-binary-search/
        '''
        arr = self.__items
        low = 0
        high = len(arr) - 1
        mid = 0

        while low <= high:
            mid = (high+low) // 2
            if arr[mid].f_value < value.f_value:
                if mid + 1 > high or arr[mid + 1].f_value > value.f_value:
                    return mid + 1
                low = mid + 1
            elif arr[mid].f_value > value.f_value:
                if mid - 1 < low:
                    return mid
                if arr[mid - 1].f_value < value.f_value:
                    return mid
                high = mid - 1
            else:
                return mid
        return -1

    def insert(self, new_node: Node):
        '''Inserting the Node object'''
        index = self.__binary_search(new_node)
        self.__items.insert(index, new_node)

    def delete(self, pos: int):
        '''
        Removes the Node with specific id
        Per now, it is gonna be O(n)
        '''
        for i, item in enumerate(self.__items):
            if item.position == pos:
                del self.__items[i]
                return

    def pop(self, index: int=-1):
        '''
        Removes the element at a specific index
        and returns it
        By default it will remove the last element
        '''
        return self.__items.pop(index)

    def get(self, pos: int=None):
        '''Check if a Node exist in the list (same position)'''
        if pos is None:
            return True, self.__items
        for node in self.__items:
            if node.position == pos:
                return True, node
        return False, None

    def get_by_index(self, index: int=None):
        '''Returns the list'''
        if index is None:
            return self.__items
        return self.__items[index]

    def __len__(self):
        '''Returns the length'''
        return len(self.__items)
