'''
Driving class, containing the different states.
'''
from typing import List
# pylint: disable=C0413
try:
    from pathfinding.pathfinding import PathFinding
    from qr_code.qr_code import QRCode
    from line_detection.parking_slot_detection import ParkingSlotDetector
except ImportError:
    from computer_vision.pathfinding.pathfinding import PathFinding
    from computer_vision.qr_code.qr_code import QRCode
    from computer_vision.line_detection.parking_slot_detection import ParkingSlotDetector

class Driving:
    '''Driving class'''
    def __init__(self, conf: dict, pathfinding: PathFinding, qr_code: QRCode):
        '''Init'''
        self.conf = conf
        self.pathfinding = pathfinding
        self.qr_code = qr_code

        # ----- PARKING SLOT DETECTOR ----- #
        P_CANNY = [50, 100]
        P_HOUGH = [80, 200, 5]
        P_ITERATIONS = [5, 2]
        P_BLUR = 7
        P_FILTER_ATOL = [20, 20]
        P_CLUSTER_ATOL = 0

        self.parking_slot_detector = ParkingSlotDetector(
            canny=P_CANNY,
            hough=P_HOUGH,
            blur=P_BLUR,
            iterations=P_ITERATIONS,
            filter_atol=P_FILTER_ATOL,
            cluster_atol=P_CLUSTER_ATOL
        )

    def driving(self, frame, frame_dimensions):
        '''Driving'''
        objects: List[self.pathfinding.Objects] = []
        # ----- QR CODE ----- #
        current_qr_data = self.qr_code.get_data(frame)
        if current_qr_data['ret']:
            # assuming only one qr code
            distance_y = current_qr_data['distances'][0]
            distance_x = self.qr_code.qr_geometries[0].get_qr_code_distance_x(
                (frame_dimensions[0]/2, frame_dimensions[1]/2))
            new_object: PathFinding.Objects = {
                 'values': [(distance_x, distance_y)],
                 'distance': True,
                 'object_id': self.conf['object_id']['QR']
            }
            objects.append(new_object)
            line_dict = self.parking_slot_detector.get_parking_slot(frame, current_qr_data)
            if line_dict is not None:
                for lines in line_dict['all_lines']:
                    objects.append({
                        'values':[(lines[0], lines[1]), (lines[2], lines[3])],
                        'distance': False,
                        'object_id': 30})
                for lines in line_dict['slot_lines']:
                    objects.append({
                        'values': [(lines[0], lines[1]), (lines[2], lines[3])],
                        'distance': False,
                        'object_id': 30})

        self.pathfinding.insert_objects(objects)
        start_id = self.conf['object_id']['car']
        end_id = self.conf['object_id']['QR']
        path_data = self.pathfinding.calculate_path(start_id, end_id)
        return path_data

    def waiting(self):
        '''Waiting'''

    def parking(self):
        '''Parking'''

    def stopping(self):
        '''Stopping'''
