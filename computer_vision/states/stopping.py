
from stop_sign_detection.stop_sign_detector import StopSignDetector

class StopSignAction():
    '''Class for waiting state'''
    def __init__(self, path) -> None:
        self.stop_sign_detector = StopSignDetector(path)

    def run_calculation(self, input_data):
        '''Take frame input and output relevant data'''
        current_stop_sign = self.stop_sign_detector.detect_signs(input_data)
        if len(current_stop_sign) > 0:
            distance = self.stop_sign_detector.get_distance(current_stop_sign[0]) * 1000
            if distance < 4.5:
                print("STOPPING")
                return len(current_stop_sign), {
                    "dir_0" : 0,
                    "dir_1" : 0,
                    "speed_0" : 0,
                    "speed_1" : 0
                }
            print(f"Distance: {distance}, sign: {current_stop_sign}")
            return len(current_stop_sign), {
                "dir_0" : 0,
                "dir_1" : 0,
                "speed_0" : 10,
                "speed_1" : 10
        }
        return 0, {
                "dir_0" : 0,
                "dir_1" : 0,
                "speed_0" : 10,
                "speed_1" : 10
        }
