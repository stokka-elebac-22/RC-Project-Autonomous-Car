'''Parking class'''
from environment.src.a_star import AStar
from pathfinding.pathfinding import PathFinding
from line_detection.parking_slot_detection import ParkingSlotDetector
from qr_code.qr_code import QRCode

class ParkingAction():
    '''Class for autonomous parking state'''

    def __init__(self, conf, env) -> None:
        self.conf = conf
        a_star = AStar(weight=2, penalty=2, hindrance_ids=[1, 30])
        self.path_finding = PathFinding(
            env,
            a_star,
            0.5,
            conf['velocity']
        )
        self.parking_slot_detector = ParkingSlotDetector(
            conf['parking']['canny'],
            conf['parking']['blur'],
            conf['parking']['hough'],
        )
        self.qr_code = QRCode(conf['qr_code_size'])
        self.env = env

    def run_calculation(self, input_data):
        '''Take frame input and output relevant data'''
        # Use lane Module
        self.path_finding.reset()
        obstacles = []

        qr_data = self.qr_code.get_data(input_data)
        if qr_data['ret']:
            distances = self.env.point_to_distance(
                (qr_data['points'][0][0][0]+
                 (qr_data['points'][0][1][0]-qr_data['points'][0][0][0])/2,
                 qr_data['points'][0][0][0]))
            qr_distance_x = distances[0]
            qr_distance_y = qr_data['distances'][0]
            obstacles.append({'values': [
                (qr_distance_x, qr_distance_y)],
                'distance': True, 'object_id': 20})

            # Use ParkingSlot Module
            qr_code_data = {
                'ret': qr_data['ret'],
                'points': qr_data['points']
            }

            line_dict = self.parking_slot_detector.get_parking_slot(input_data, qr_code_data)
            if line_dict is not None:
                for lines in line_dict['all_lines']:
                    obstacles.append({'values': [
                        (lines[0], lines[1]), (lines[2], lines[3])],
                        'distance': False, 'object_id': 30})
                for lines in line_dict['slot_lines']:
                    obstacles.append({'values': [
                        (lines[0], lines[1]), (lines[2], lines[3])],
                        'distance': False, 'object_id': 30})
        self.path_finding.insert_objects(obstacles)
        path_data = self.path_finding.calculate_path(
            self.conf['object_id']['car'], self.conf['object_id']['QR'])
        if path_data is None:
            print('There is not path data...')
            return 0, None

        return len(path_data), path_data



