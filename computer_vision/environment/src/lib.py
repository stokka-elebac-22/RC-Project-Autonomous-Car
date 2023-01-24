'''Library'''
import dataclasses
import pygame as pg

class Objects:
    '''Class over all the objects'''
    def __init__(self):
        self.objects = TwoWayDict()
        self._init_objects()
        self.object_color = {}
        self._init_object_colors()

    def _init_objects(self):
        '''Initializing the object dict'''
        obj = [
            ('None', 0)
        ]
        for i in obj:
            self.objects[i[0]] = i[1]

    def _init_object_colors(self):
        obj = [
            (0, pg.Color(255, 255, 255))
        ]
        for i in obj:
            self.object_color[i[0]] = i[1]


    def get_color(self, obj):
        '''Get the color of the object'''
        if isinstance(obj, int):
            obj = self.objects[object]
        return self.objects_color.get(object)



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
