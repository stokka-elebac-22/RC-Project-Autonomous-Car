'''
Driving class, containing the different states.
'''
import os
import sys
from typing import List
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
# pylint: disable=C0413
from computer_vision.pathfinding.pathfinding import PathFinding
from computer_vision.qr_code.qr_code import QRCode
class Driving:
    '''Driving class'''
    def __init__(self, conf: dict, pathfinding: PathFinding, qr_code: QRCode):
        '''Init'''
        self.conf = conf
        self.pathfinding = pathfinding
        self.qr_code = qr_code

    def driving(self, frame):
        '''Driving'''
        objects: List[self.pathfinding.Objects] = []
        # ----- QR CODE ----- #
        current_qr_data = self.qr_code.get_data(frame)
        if current_qr_data['ret']:
            # assuming only one qr code
            distance_y = current_qr_data['distances'][0]
            distance_x = self.qr_code.qr_geometries.get_qr_code_distance_x()
            new_object: PathFinding.Objects = {
                 'values': [(distance_x, distance_y)],
                 'distance': True,
                 'object_id': self.conf['object_id']['QR']
            }
            objects.append(new_object)
        self.pathfinding.insert_objects(objects)

    def waiting(self):
        '''Waiting'''

    def parking(self):
        '''Parking'''

    def stopping(self):
        '''Stopping'''
