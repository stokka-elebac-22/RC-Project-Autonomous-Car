'''main_headless.py: DATBAC23 Car system main.'''

import sys
from defines import States
from socket_handling.abstract_server import NetworkSettings
from socket_handling.multi_socket_server import MultiSocketServer
from camera_handler.camera_headless import CameraHandler
from camera_handler.camera_sock_server import CamSocketStream
from traffic_sign_detection.main import TrafficSignDetector
from qr_code.qr_code import QRCode
import numpy as np

class Headless():
    '''Class handling headless running'''
    def __init__(self, conf: dict):
        self.state = States.WAITING  # Start in "idle" state

        # Network config for main connection + camera(s)
        self.net_main = NetworkSettings(conf["network"]["host"], conf["network"]["port"])
        self.net_cam0 = NetworkSettings(conf["network"]["host"], conf["network"]["port_cam0"])
        self.net_cam1 = NetworkSettings(conf["network"]["host"], conf["network"]["port_cam1"])

        # Start main socket server for connections
        self.socket_server = MultiSocketServer(self.net_main)
        self.socket_server.start()

        self.cam0_stream = CamSocketStream(self.net_cam0)
        if conf["network"]["stream_en_cam0"] is True:
            self.cam0_stream.start()

        self.cam1_stream = CamSocketStream(self.net_cam1)
        if conf["network"]["stream_en_cam1"] is True:
            self.cam1_stream.start()

        # Get size from config
        size = {
            'px': conf["camera0"]["size"]["px"],
            'mm': conf["camera0"]["size"]["mm"],
            'distance': conf["camera0"]["size"]["distance"],
        }

        self.cam0_handler = CameraHandler(conf["camera0"]["id"])

        self.qr_code = QRCode(size)
        self.stop_sign_detector = TrafficSignDetector('stop_sign_model.xml')

        while True:
            # Take new picture, handle socket transfers
            ret, frame0 = self.cam0_handler.get_cv_frame()
            if ret is True:
                self.cam0_stream.send_to_all(frame0)
                self.cam1_stream.send_to_all(frame0)

            if self.state is States.WAITING:  # Prints detected data (testing)
                current_qr_data = self.qr_code.get_data(frame0)
                output_data = 'Data: \n'
                # print(current_qr_data)
                if current_qr_data['ret']:
                    for i in range(len(current_qr_data['distances'])):
                        output_data += \
                            f"QR-Code {str(i)} \n \
                                Distance: {round(current_qr_data['distances'][i])} \n \
                                Angle: {current_qr_data['angles'][i]} \n"

                        output_data += 'Data: ' + current_qr_data['info'][i] + '\n'

                current_stop_sign = self.stop_sign_detector.detect_signs(frame0)
                if current_qr_data['distances'] is not None and len(current_qr_data['distances']) > 0:
                    print(output_data)
                if len(current_stop_sign) > 0:
                    print(current_stop_sign)

            elif self.state is States.PARKING:
                pass
            elif self.state is States.DRIVING:
                pass

