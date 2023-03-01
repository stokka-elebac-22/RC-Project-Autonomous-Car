'''main_headless.py: DATBAC23 Car system main.'''

import sys
from typing import Tuple
from defines import States
from socket_handling.multi_socket_server import MultiSocketServer
from camera_handler.camera_handler import CameraHandler, VideoThread
from traffic_sign_detection.main import TrafficSignDetector
from qr_code.qr_code import QRCode
import numpy as np

# Run in thread, not qthread?
# class Worker(QObject, ):  # pylint: disable=R0903
#     '''Worker thread'''
#     finished = pyqtSignal()
#     def __init__(self, cam_handler: CameraHandler):
#         self.cam_handler = cam_handler
#         super().__init__()

#     def update_webcam_list(self):
#         '''Long-running task.'''
#         self.cam_handler.refresh_camera_list()
#         self.finished.emit()


class Headless():
    '''Class handling headless running'''
    def __init__(self, connection: Tuple[str, int]):
        self.state = States.WAITING
        self.socket_server = MultiSocketServer()
        self.connection_details = connection
        self.camera_handler = CameraHandler()
        # Create an instance of QtWidgets.QApplication

        # Get size from config
        size = {
            'px': 76,
            'mm': 52,
            'distance': 500,
        }

        self.qr_code = QRCode(size)
        self.stop_sign_detector = TrafficSignDetector('stop_sign_model.xml')

        self.refresh_webcam_list()

        '''Possible logic:'''
        while True:
            '''Handle things happening, request/take new picture?'''
            match self.state:
                case States.WAITING:
                    pass
                case States.PARKING:
                    pass
                case States.DRIVING:
                    pass

    '''Or, run logic on new image from camera similar to pyQt way'''
    #@pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        '''Updates the image_label with a new opencv image'''
        output_frame = cv_img
        qt_img = self.camera_handler.convert_cv_qt(
            cv_img, self.img_input[0].width(), self.img_input[0].height())
        current_qr_data = self.qr_code.get_data(cv_img)
        output_data = 'Data: \n'
        # print(current_qr_data)
        if current_qr_data['ret']:
            self.qr_code.display(output_frame, current_qr_data, verbose=0)
            for i in range(len(current_qr_data['distances'])):
                output_data += \
                    f"QR-Code {str(i)} \n \
                        Distance: {round(current_qr_data['distances'][i])} \n \
                        Angle: {current_qr_data['angles'][i]} \n"

                output_data += 'Data: ' + current_qr_data['info'][i] + '\n'

        current_stop_sign = self.stop_sign_detector.detect_signs(cv_img)
        self.stop_sign_detector.show_signs(output_frame, current_stop_sign)

        output_img = self.camera_handler.convert_cv_qt(
            cv_img, self.img_output.width(), self.img_output.height())

        # print('Setting new image')
        self.img_input[0].setPixmap(qt_img)
        self.img_output.setPixmap(output_img)
        self.output_text.setText(output_data)


    def callback_func_update_camera_cbo(self):
        '''Callback function for webcam check thread'''
        for cbo in self.camera_cbo:
            for camera in self.camera_handler.get_camera_list():
                cbo.addItem(
                    self.camera_handler.get_camera_string(camera['id']))
                # create the video capture thread
        self.thread2 = VideoThread(1)  # pylint: disable=W0201
        # connect its signal to the update_image slot
        self.thread2.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread2.start()
    # def update_plot_data(self):
