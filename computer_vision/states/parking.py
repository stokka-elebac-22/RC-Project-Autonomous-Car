from line_detection.parking_slot_detection import parking_slot_detector
from qr_code.qr_code import QRCode

class ParkingAction():
    '''Class for waiting state'''

    def __init__(self, conf_parking, conf_qr, env) -> None:
        self.parking_slot_detector = parking_slot_detector(
            conf_parking['canny'],
            conf_parking['blur'],
            conf_parking['hough'],
        )
        self.r_code = QRCode(conf_qr)
        self.env = env

    def run_calculation(self, input_data):
        '''Take frame input and output relevant data'''
        # Use lane Module
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

            line_dict = parking_slot_detector.get_parking_slot(input_data, qr_code_data)
            if line_dict is not None:
                for lines in line_dict['all_lines']:
                    obstacles.append({'values': [
                        (lines[0], lines[1]), (lines[2], lines[3])],
                        'distance': False, 'object_id': 30})
                for lines in line_dict['slot_lines']:
                    obstacles.append({'values': [
                        (lines[0], lines[1]), (lines[2], lines[3])],
                        'distance': False, 'object_id': 30})
            
        return obstacles



