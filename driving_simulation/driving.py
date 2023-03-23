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
from computer_vision.qr_code.qr_code import QRCode
class Driving:
    '''Driving class'''
    def __init__(self, pathfinding: PathFinding, qr_code: QRCode):
        '''Init'''
        self.pathfinding = pathfinding
        self.qr_code = qr_code

    def driving(self):
        '''Driving'''


    def waiting(self):
        '''Waiting'''

    def parking(self):
        '''Parking'''

    def stopping(self):
        '''Stopping'''
