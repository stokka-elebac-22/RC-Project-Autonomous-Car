
from stop_sign_detection.stop_sign_detector import StopSignDetector
from qr_code.qr_code import QRCode

class WaitingState():
    '''Class for waiting state'''
    def __init__(self, size) -> None:
        self.qr_code = QRCode(size)
        self.stop_sign_detector = StopSignDetector('stop_sign_model.xml')

    def run_calculation(self, input_data):
        '''Take frame input and output relevant data'''
        current_qr_data = self.qr_code.get_data(input_data)
        output_data = 'Data: \n'
        # print(current_qr_data)
        if current_qr_data['ret']:
            for i in range(len(current_qr_data['distances'])):
                output_data += \
                    f"QR-Code {str(i)} \n \
                        Distance: {round(current_qr_data['distances'][i])} \n \
                        Angle: {current_qr_data['angles'][i]} \n"

                output_data += 'Data: ' + current_qr_data['info'][i] + '\n'

        current_stop_sign = self.stop_sign_detector.detect_signs(input_data)
        if current_qr_data['distances'] is not None and \
                len(current_qr_data['distances']) > 0:
            print(output_data)
        if len(current_stop_sign) > 0:
            print(current_stop_sign)
        return {
            "dir_0" : 0,
            "dir_1" : 0,
            "speed_0" : 0,
            "speed_1" : 0
        }
