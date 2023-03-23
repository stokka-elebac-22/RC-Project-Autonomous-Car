'''
defines.py Class for enums to ensure consistency in valus across platforms.
'''
from enum import Enum

class States(Enum):
    '''Enum for states'''
    WAITING = 0
    PARKING = 1
    DRIVING = 2
    STOPPING = 3