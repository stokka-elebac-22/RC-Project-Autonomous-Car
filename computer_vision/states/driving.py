from line_detection.lane_detection import LaneDetector

class LaningAction():
    '''Class for waiting state'''

    def __init__(self, conf) -> None:
        self.lane_detector = LaneDetector(
            conf['canny'],
            conf['blur'],
            conf['hough'],
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
            
        return obstacles



