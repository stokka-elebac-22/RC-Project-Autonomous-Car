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
import struct
from defines import States
from socket_handling.abstract_server import NetworkSettings
from socket_handling.db_handler import DbHandler
from socket_handling.socket_client import SocketClient # pylint: disable=W0611
from camera_handler.socket_video_thread import SocketVideoThread
from camera_handler.camera_handler import CameraHandler, VideoThread
from joystick_handler.joystick_module import JoystickHandler
from joystick_handler.joystick_position import CurrentHeading
from stop_sign_detection.stop_sign_detector import StopSignDetector
from qr_code.qr_code import QRCode
from PyQt6 import QtWidgets, QtGui, uic, QtCore
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import numpy as np
from pygame.locals import * # pylint: disable=W0401

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
        self.conf = conf
        self.connection_details = conf["network"]
        self.storage = DbHandler('data.db')
        self.socket_client = SocketClient(self.storage)
        self.camera_handler = CameraHandler()
        self.joystick_handler = JoystickHandler()
        self.fps_count = 0
        self.output_data = ''
        self.joystick_position = CurrentHeading()
        # Create an instance of QtWidgets.QApplication
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setWindowIcon(QtGui.QIcon('car_ico.ico'))

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
        self.chk_computer_vision = [
            self.findChild(QtWidgets.QCheckBox, 'chk_linedetect'),
            self.findChild(QtWidgets.QCheckBox, 'chk_objectdetect'),
            self.findChild(QtWidgets.QCheckBox, 'chk_disparity'),
            self.findChild(QtWidgets.QCheckBox, 'chk_qrdetect'),
            self.findChild(QtWidgets.QCheckBox, 'chk_stop_sign')
        ]

        self.cam_thread = ["", ""]
        self.chk_enable[0].stateChanged.connect(
            lambda: self.check_and_start_camera(self.chk_enable[0], 0))
        self.chk_enable[1].stateChanged.connect(
            lambda: self.check_and_start_camera(self.chk_enable[1], 1))

        self.cbo_car_state = self.findChild(QtWidgets.QComboBox, 'cbo_car_state')
        for state in States:
            self.cbo_car_state.addItem(f'{state.value}: {state.name}')

        self.cbo_socket_conn = self.findChild(QtWidgets.QComboBox, 'cbo_socket_connection')
        for conn in self.connection_details['host_list']:
            print(conn['name'])
            self.cbo_socket_conn.addItem(f"{conn['name']}: {conn['host']}")
        self.btn_connect = self.findChild(QtWidgets.QPushButton, 'btn_connect')
        self.btn_connect.clicked.connect(
            lambda: self.socket_connect(self.cbo_socket_conn.currentIndex()))

        self.cbo_state = self.findChild(QtWidgets.QComboBox, 'cbo_car_state')
        self.btn_send_state = self.findChild(QtWidgets.QPushButton, 'btn_setstate')
        self.btn_send_state.clicked.connect(
            lambda: self.socket_send_state(self.cbo_state.currentIndex()))

        # Get size from config
        size = {
            'px': conf["camera0"]["size"]["px"],
            'mm': conf["camera0"]["size"]["mm"],
            'distance': conf["camera0"]["size"]["distance"],
        }

        self.qr_code = QRCode(size)
        self.stop_sign_detector = StopSignDetector('stop_sign_model.xml')

        self.img_output = self.findChild(QtWidgets.QLabel, 'output_img')
        self.output_text = self.findChild(QtWidgets.QLabel, 'lbl_data_output')
        self.refresh_webcam_list()

        print(self.joystick_handler.available_joystick_list)
        self.joystick_handler.set_joystick(0)
        self.joystick_handler.start()
        self.joystick_handler.change_pixmap_signal.connect(self.joystick_callback)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_plots_and_label_data)
        self.timer.start()

        self.update_plots_and_label_data()

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
            else: # Fix settings for camera stream + add support for 2 cameras
                self.cam_thread[index] = SocketVideoThread(NetworkSettings("192.168.121.57", 2005))
                if index == 0:
                    self.cam_thread[index].change_pixmap_signal.connect(self.update_image)
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
        '''Updates the image_label with a new OpenCV image'''
        self.fps_count += 1
        qr_output = ''
        output_frame = cv_img
        qt_img = self.camera_handler.convert_cv_qt(
            cv_img, self.img_input[0].width(), self.img_input[0].height())

        ## QR Code
        if self.chk_computer_vision[3].isChecked():
            current_qr_data = self.qr_code.get_data(cv_img)
            # print(current_qr_data)
            if current_qr_data['ret']:
                self.qr_code.display(output_frame, current_qr_data, verbose=0)
                for i in range(len(current_qr_data['distances'])):
                    qr_output += \
                        f"-QR-Code {str(i)} \n \
                            Distance: {round(current_qr_data['distances'][i], 5)} \
                            Angle: {round(current_qr_data['angles'][i], 5)} \n  \
                            Data: {current_qr_data['info'][i]}"

        ## Stop sign detection
        if self.chk_computer_vision[4].isChecked():
            current_stop_sign = self.stop_sign_detector.detect_signs(cv_img)
            self.stop_sign_detector.show_signs(output_frame, current_stop_sign)

        ## Adjust output image to fit frame
        output_img = self.camera_handler.convert_cv_qt(
            cv_img, self.img_output.width(), self.img_output.height())

        # Set new frame
        self.img_input[0].setPixmap(qt_img)
        self.img_output.setPixmap(output_img)

        # Ready current data
        self.output_data = 'Data:\n ' + qr_output

    def update_image2(self, cv_img):
        '''Updates image2 with a new opencv image'''
        qt_img = self.camera_handler.convert_cv_qt(
            cv_img, self.img_input[0].width(), self.img_input[0].height())
        # Update frame 2
        self.img_input[1].setPixmap(qt_img)

    def joystick_callback(self, event_type):
        '''Callback for joystick signals'''
        if event_type == JOYAXISMOTION: # pylint: disable=E0602
            self.joystick_position.update_direction(
                self.joystick_handler.event_num,
                self.joystick_handler.axis[self.joystick_handler.event_num])
        elif event_type == JOYBALLMOTION: # pylint: disable=E0602
            print(event_type)
            print(self.joystick_handler.event_num)
            print(self.joystick_handler.ball[self.joystick_handler.event_num])
        elif event_type == JOYHATMOTION: # pylint: disable=E0602
            print(event_type)
            print(self.joystick_handler.event_num)
            print(self.joystick_handler.joy[self.joystick_handler.event_num])
        elif event_type == JOYBUTTONUP: # pylint: disable=E0602
            self.joystick_position.update_button(
                self.joystick_handler.event_num, 0)
        elif event_type == JOYBUTTONDOWN: # pylint: disable=E0602
            self.joystick_position.update_button(
                self.joystick_handler.event_num, 1)

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

    def update_plots_and_label_data(self):
        '''Update plots and label data'''
        if self.fps_count > 0:
            self.output_data += f'\nFPS: {self.fps_count * 2}'
            self.fps_count = 0
            self.output_text.setText(self.output_data) # pylint: disable=E0001
        if self.joystick_handler.joystick_active and self.socket_client.running:
            self.socket_send_joystick_direction()

    def socket_connect(self, connection_id: int):
        '''Start socket client connection'''
        if not self.socket_client.running:
            host = self.connection_details['host_list'][connection_id]['host']
            port = self.connection_details['host_list'][connection_id]['port']
            conn = NetworkSettings(host, port)
            self.socket_client.start(conn)
        else:
            print("Already connected!")

    def socket_send_state(self, state: int):
        '''Send state request on socket connection '''
        if self.socket_client.running:
            data = struct.pack("I", 1 + state*256) # States.CMD_SET_STATE.value
            print(f"Sending state: {state} as {data}")
            self.socket_client.send_to_all(data)
        else:
            print("Not connected!")

    def socket_send_joystick_direction(self):
        '''Send joystick direction update on socket connection '''
        if self.socket_client.running:  # States.CMD_JOYSTICK_DIRECTIONS.value = 2
            data = self.joystick_position.get_byte_for_heading(2)
            print("Sending data")
            self.socket_client.send_to_all(data)
        else:
            print("Not connected!")
