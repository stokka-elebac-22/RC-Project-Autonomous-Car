'''Library'''
import dataclasses
import pygame as pg

@dataclasses.dataclass
class Colors:
    '''Pygame colors'''
    def __init__(self):
        self.black = pg.Color(0, 0, 0)
        self.white = pg.Color(255, 255, 255)
        self.red = pg.Color(255, 0, 0)
        self.green = pg.Color(0, 255, 0)
        self.blue = pg.Color(0, 0, 255)


class Objects:
    '''Class over all the objects'''
    def __init__(self):
        self.objects = TwoWayDict()

    def get_color(self, object):
        '''Get the color of the object'''
        


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