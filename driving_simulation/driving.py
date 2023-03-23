'''
Driving class, containing the different states.
'''
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
# pylint: disable=C0413
from computer_vision.pathfinding.pathfinding import PathFinding
class Driving:
    '''Driving class'''
    def __init__(self, pathfinding: PathFinding):
        '''Init'''
        self.pathfinding = pathfinding

    def driving(self):
        '''Driving'''


    def waiting(self):
        '''Waiting'''

    def parking(self):
        '''Parking'''

    def stopping(self):
        '''Stopping'''
