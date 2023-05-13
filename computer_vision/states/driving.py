'''Driving state'''
from environment.src.a_star import AStar
from pathfinding.pathfinding import PathFinding
from line_detection.lane_detection import LaneDetector

class LaningAction():
    '''Class for Lane driving state'''

    def __init__(self, conf, env) -> None:
        self.conf = conf
        a_star = AStar(weight=2, penalty=2, hindrance_ids=[1, 30])
        self.path_finding = PathFinding(
            env,
            a_star,
            0.5,
            conf['velocity']
        )
        self.lane_detector = LaneDetector(
            conf['lane']['canny'],
            conf['lane']['blur'],
            conf['lane']['hough'],
        )

    def run_calculation(self, input_data):
        '''Take frame input and output relevant data'''
        # Use lane Module
        obstacles = []
        avg_lines = self.lane_detector.get_lane_line(input_data)
        if avg_lines is not None:
            for line in avg_lines:
                if line is not None:
                    obstacles.append({'values': [
                                     (line[0], line[1]), (line[2], line[3])],
                        'distance': False, 'object_id': 31})

            check_point = self.lane_detector.get_next_point(input_data, avg_lines)
            if check_point is not None:
                obstacles.append({'values': [
                    check_point],
                    'distance': False, 'object_id': 20})
        self.path_finding.reset()
        self.path_finding.insert_objects(obstacles)
        path_data = self.path_finding.calculate_path(
            self.conf['object_id']['car'], self.conf['object_id']['QR'])
        if path_data is None:
            print('There is not path data...')


        return obstacles



