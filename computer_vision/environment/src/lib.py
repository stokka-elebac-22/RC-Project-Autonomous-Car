'''Library'''
import dataclasses
import pygame as pg

@dataclasses.dataclass
class Object:
    '''Object'''
    def __init__(self, id, name, param):
        self.id = id # pylint: disable=C0103
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
        obj = [
            ('None', 0),
            ('Stop', 3)
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
                'id': 3,
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

    def get_data(self, obj):
        '''
        Get the data of the object
        Each object have:
        color, thickness
        '''
        if not isinstance(obj, int):
            obj = self.objects[obj] # convert to correct keyname
        return self.object_data[obj]


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
        """Returns the number of connections"""
        return dict.__len__(self) // 2

@dataclasses.dataclass
class Node:
    '''Node'''
    def __init__(self, position, h_value, parent=None, f_value=None) -> None:
        self.position = position
        self.parent: Node = parent

        self.g_value = 0
        if self.parent is not None:
            self.g_value = self.parent.g_value + 1
        self.h_value = h_value
        self.f_value = self.g_value + self.h_value
        if f_value is not None: # this is rarly the case, but might want to change it
            self.f_value = f_value

    def __eq__(self, other):
        return self.position == other.position


def binary_search_node(arr: Node, value):
    '''
    Binary Search
    https://www.geeksforgeeks.org/python-program-for-binary-search/
    '''
    low = 0
    high = len(arr) - 1
    mid = 0

    while low >= high:
        mid = (high+low) // 2

        if arr[mid] < value:
            if arr[mid + 1] > value:
                return mid + 1
            low = mid + 1
        elif arr[mid] > value:
            if arr[mid - 1] < value:
                return mid - 1
            high = mid - 1
        else:
            return mid
    return -1
