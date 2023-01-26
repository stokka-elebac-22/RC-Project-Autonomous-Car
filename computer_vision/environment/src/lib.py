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
            ('Hindrance', 1),
            ('Path', 2),
            ('Stop', 3),
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
                'name': 'Path',
                'param': {
                    'color': pg.Color(50, 80, 180),
                    'thickness': 0
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
        if not isinstance(obj, (int, float)):
            obj = self.objects[obj] # convert to correct keyname
        return self.object_data[int(obj)]


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

@dataclasses.dataclass
class Node:
    '''Node'''
    # newid = itertools.count().__next__
    def __init__(self, position, h_value, parent=None, f_value=None) -> None:
        # self.id = Node.newid() # pylint: disable=C0103
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
        if self.position != other.position or \
            self.g_value != other.g_value or \
            self.h_value != other.h_value or \
            self.f_value != other.f_value:
            return False

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
                    return mid - 1
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

    def contains(self, pos):
        '''Check if a Node exist in the list (same position)'''
        for node in self.__items:
            if node.position == pos:
                return True
        return False

    def get(self, index: int=None):
        '''Returns the list'''
        if index is None:
            return self.__items
        return self.__items[index]

    def __len__(self):
        '''Returns the length'''
        return len(self.__items)

    def __eq__(self, other):
        '''Equal'''
        for val1, val2 in zip(self.__items, other):
            if val1 != val2:
                return False
        return True
