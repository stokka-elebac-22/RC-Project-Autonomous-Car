'''
Driving class, containing the different states.
'''
from typing import List
# pylint: disable=C0413
try:
    from collections import deque
    from pathfinding.pathfinding import PathFinding
    from qr_code.qr_code import QRCode
    from line_detection.lane_detection import LaneDetector
    from line_detection.parking_slot_detection import ParkingSlotDetector
    from traffic_sign_detection.traffic_sign_detector import TrafficSignDetector
except ImportError:
    from computer_vision.pathfinding.pathfinding import PathFinding
    from computer_vision.qr_code.qr_code import QRCode
    from computer_vision.line_detection.lane_detection import LaneDetector
    from computer_vision.line_detection.parking_slot_detection import ParkingSlotDetector
    from computer_vision.traffic_sign_detection.traffic_sign_detector import TrafficSignDetector


class DrivingStates:
    '''DrivingStates class'''

    def __init__(self, conf: dict,
                 pathfinding: PathFinding,
                 qr_code: QRCode,
                 stop_sign_detector: TrafficSignDetector,
                 parking_slot_detector: ParkingSlotDetector,
                 lane_detector: LaneDetector
                 ): # pylint: disable=R0913
        '''Init'''
        self.conf = conf
        self.pathfinding = pathfinding
        self.qr_code = qr_code
        self.stop_sign_detector = stop_sign_detector
        self.parking_slot_detector = parking_slot_detector
        self.lane_detector = lane_detector

    def simulation(self, frame, frame_dimensions):
        '''Simulation'''
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
        self.pathfinding.insert_objects(objects)
        start_id = self.conf['object_id']['car']
        end_id = self.conf['object_id']['QR']
        path_data = self.pathfinding.calculate_path(start_id, end_id)
        return path_data

    def waiting(self, frame):
        '''Waiting'''
        current_stop_sign = self.stop_sign_detector.detect_signs(frame)
        if len(current_stop_sign) > 0:
            print(current_stop_sign)

        # ---------- QR-Code ---------- #
        current_qr_data = self.qr_code.get_data(frame)
        output_data = 'Data: \n'
        if current_qr_data['ret']:
            for i in range(len(current_qr_data['distances'])):
                output_data += \
                    f"QR-Code {str(i)} \n \
                        Distance: {round(current_qr_data['distances'][i])} \n \
                        Angle: {current_qr_data['angles'][i]} \n"
                output_data += 'Data: ' + current_qr_data['info'][i] + '\n'
            if current_qr_data['distances'] is not None and \
                    len(current_qr_data['distances']) > 0:
                print(output_data)

    def driving(self, frame):
        '''Driving'''
        objects: List[self.pathfinding.Objects] = []
        avg_lines = self.lane_detector.get_lane_line(frame)
        if avg_lines is not None:
            for line in avg_lines:
                if line is not None:
                    objects.append({'values': [
                                    (line[0], line[1]), (line[2], line[3])],
                                    'distance': False,
                                    'object_id': self.conf['object_id']['lane_line']})
            check_point = self.lane_detector.get_next_point(frame, avg_lines)
            if check_point is not None:
                objects.append({'values': [check_point],
                                'distance': False,
                                'object_id': self.conf['object_id']['end_point']})

                path_data = self.pathfinding.calculate_path(check_point, False)

                # ---------- UPDATE ENVIRONMENT ---------- #
                self.pathfinding.reset()
                self.pathfinding.insert_objects(objects)

                # ---------- PATH ---------- #
                path_data = self.pathfinding.calculate_path(
                self.conf['object_id']['car'], self.conf['object_id']['end_point'])

                # ---------- ACTIONS ---------- #
                if path_data is not None:
                    angles = path_data['angles']
                    times = path_data['times']
                    actions: deque = deque()
                    for angle, action_time in zip(angles, times):
                        actions.append({
                            'speed': self.conf['spline']['velocity'],
                            'angle': angle,
                            'time': action_time,
                        })
                    return actions
        return None

    def parking(self, frame, frame_dimensions): # pylint: disable=R0914
        '''Parking'''
        objects: List[self.pathfinding.Objects] = []

        ### QR Code ###
        qr_data = self.qr_code.get_data(frame)
        if not qr_data['ret']:
            return None

        current_qr_data = self.qr_code.get_data(frame)
        if current_qr_data['ret']:
            # assuming only one qr code
            distance_y = current_qr_data['distances'][0]
            distance_x = self.qr_code.qr_geometries[0].get_qr_code_distance_x(
                (frame_dimensions[0]/2, frame_dimensions[1]/2))
            qr_object: PathFinding.Objects = {
                'values': [(distance_x, distance_y)],
                'distance': True,
                'object_id': self.conf['object_id']['QR']
            }
            objects.append(qr_object)

            line_dict = self.parking_slot_detector.get_parking_slot(
                frame, qr_data)
            if line_dict is not None:
                for lines in line_dict['all_lines']:
                    objects.append({'values': [
                        (lines[0], lines[1]), (lines[2], lines[3])],
                        'distance': False, 'object_id': 30})
                for lines in line_dict['slot_lines']:
                    objects.append({'values': [
                        (lines[0], lines[1]), (lines[2], lines[3])],
                        'distance': False, 'object_id': self.conf['object_id']['parking_line']})

            # ---------- UPDATE ENVIRONMENT ---------- #
            self.pathfinding.reset()
            self.pathfinding.insert_objects(objects)

            # ---------- PATH ---------- #
            if len(current_qr_data['distances']) > 0:
                # ---------- SPLINES ---------- #
                path_data = self.pathfinding.calculate_path(
                    self.conf['object_id']['car'], self.conf['object_id']['QR'])

            # ---------- ACTIONS ---------- #
                if path_data is not None:
                    angles = path_data['angles']
                    times = path_data['times']
                    actions: deque = deque()
                    for angle, action_time in zip(angles, times):
                        actions.append({
                            'speed': self.conf['spline']['velocity'],
                            'angle': angle,
                            'time': action_time,
                        })
                    return actions
        return None

    def stopping(self, frame):
        '''Stopping'''
        actions = deque()
        current_stop_signs = self.stop_sign_detector.detect_signs(frame)
        no_sign = True
        if len(current_stop_signs) > 0:
            for sign in current_stop_signs:
                distance = self.stop_sign_detector.get_distance(sign)
                no_sign = False
                if distance <= self.conf['traffic_sign_detector']['distance']:
                    actions.append({
                                        'speed': 0,
                                        'angle': 0,
                                        'time': 0,
                                        })
            if no_sign:
                actions.append({
                    'speed': self.conf['base_speed'],
                    'angle': 0,
                    'time': 0,
                })
        return actions
