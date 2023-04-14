'''main_window_ui.py: DATBAC23 Control system Main Window UI code.'''
__author__ = 'Asbjørn Stokka'
__copyright__ = 'Copyright 2023'
__credits__ = ['Asbjørn Stokka']
__license__ = 'Apache-2.0'
__version__ = '0.1.0'
__maintainer__ = 'Asbjørn Stokka'
__email__ = 'asbjorn@maxit-as.com'
__status__ = 'Testing'

import sys
from socket_handling.socket_client import SocketClient # pylint: disable=W0611
from camera_handler.camera_handler import CameraHandler, VideoThread
from traffic_sign_detection.traffic_sign_detector import TrafficSignDetector
from qr_code.qr_code import QRCode
from defines import States
from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import numpy as np


class Worker(QObject, ):  # pylint: disable=R0903
    '''Worker thread'''
    finished = pyqtSignal()
    def __init__(self, cam_handler: CameraHandler):
        self.cam_handler = cam_handler
        super().__init__()

    def update_webcam_list(self):
        '''Long-running task.'''
        self.cam_handler.refresh_camera_list()
        self.finished.emit()


class Ui(QtWidgets.QMainWindow):  # pylint: disable=R0902
    '''Class handling Qt GUI control'''
    def __init__(self, ui_file, conf: dict, fullscreen: bool):
        self.connection_details = conf["network"]
        self.camera_handler = CameraHandler()
        # Create an instance of QtWidgets.QApplication
        self.app = QtWidgets.QApplication(sys.argv)

        super().__init__()
        # Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(ui_file, self)  # Load the .ui file

        self.camera_cbo = [
            self.findChild(QtWidgets.QComboBox, 'input_cbo_1'),
            self.findChild(QtWidgets.QComboBox, 'input_cbo_2')
        ]
        self.img_input = [
            self.findChild(QtWidgets.QLabel, 'input_img_1'),
            self.findChild(QtWidgets.QLabel, 'input_img_2')
        ]
        self.chk_enable = [
            self.findChild(QtWidgets.QCheckBox, 'input_chk_enable_1'),
            self.findChild(QtWidgets.QCheckBox, 'input_chk_enable_2')
        ]
        self.cam_thread = ["", ""]
        self.chk_enable[0].stateChanged.connect(
            lambda: self.check_and_start_camera(self.chk_enable[0], 0))
        self.chk_enable[1].stateChanged.connect(
            lambda: self.check_and_start_camera(self.chk_enable[1], 1))

        self.cbo_car_state = self.findChild(QtWidgets.QComboBox, 'cbo_car_state')
        for state in States:
            self.cbo_car_state.addItem('{}: {}'.format(state.value, state.name))

        self.cbo_socket_conn = self.findChild(QtWidgets.QComboBox, 'cbo_socket_connection')
        for conn in self.connection_details['host_list']:
            print(conn['name'])
            self.cbo_socket_conn.addItem('{}: {}'.format(conn['name'], conn['host']))

        # Get size from config
        size = {
            'px': conf["camera0"]["size"]["px"],
            'mm': conf["camera0"]["size"]["mm"],
            'distance': conf["camera0"]["size"]["distance"],
        }

        self.qr_code = QRCode(size)
        self.stop_sign_detector = TrafficSignDetector('stop_sign_model.xml')

        self.img_output = self.findChild(QtWidgets.QLabel, 'output_img')
        self.output_text = self.findChild(QtWidgets.QLabel, 'lbl_data_output')
        self.refresh_webcam_list()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        # self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        # self.update_plot_data()

        if fullscreen:
            self.showFullScreen()
        self.show()
        self.app.exec()

    def check_and_start_camera(self, chk_box: QtWidgets.QCheckBox, index):
        '''Trigger start of camera if checked '''
        if chk_box.isChecked() is True:
            self.camera_cbo[index].setEnabled(False)
            current_index = self.camera_cbo[index].currentIndex()
            if 'Cam' in self.camera_cbo[index].currentText():
                self.cam_thread[index] = VideoThread(current_index)  # pylint: disable=W0201
                # connect its signal to the update_image slot
                if index == 0:
                    self.cam_thread[index].change_pixmap_signal.connect(self.update_image)
                elif index == 1:
                    self.cam_thread[index].change_pixmap_signal.connect(self.update_image2)
                # start the thread
                self.cam_thread[index].start()
        else:
            try:
                self.camera_cbo[index].setEnabled(True)
                self.cam_thread[index].stop()
            except AttributeError:
                pass
            except Exception as error: # pylint: disable=W0703
                print(error)

    @pyqtSlot(np.ndarray)
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

    def update_image2(self, cv_img):
        '''Updates image2 with a new opencv image'''
        qt_img = self.camera_handler.convert_cv_qt(
            cv_img, self.img_input[0].width(), self.img_input[0].height())
        # print('Setting new image')
        self.img_input[1].setPixmap(qt_img)

    def refresh_webcam_list(self):
        '''Run a Qthread to check possible webcams and create a list'''
        self.thread = QThread()
        self.worker = Worker(self.camera_handler)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.update_webcam_list)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        self.thread.finished.connect(
            self.callback_func_update_camera_cbo
        )

    def callback_func_update_camera_cbo(self):
        '''Callback function for webcam check thread'''
        for cbo in self.camera_cbo:
            for camera in self.camera_handler.get_camera_list():
                cbo.addItem(
                    self.camera_handler.get_camera_string(camera['id']))
            cbo.addItem("Network stream cam 0")
            cbo.addItem("Network stream cam 1")
                # create the video capture thread
        self.check_and_start_camera(self.chk_enable[0], 0)
        self.check_and_start_camera(self.chk_enable[1], 1)

    # def update_plot_data(self):
