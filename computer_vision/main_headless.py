'''main_headless.py: DATBAC23 Car system main.'''
from defines import States, MessageId
from socket_handling.abstract_server import NetworkSettings
from socket_handling.multi_socket_server import MultiSocketServer
from camera_handler.camera_headless import CameraHandler
from camera_handler.camera_sock_server import CamSocketStream
from stop_sign_detection.stop_sign_detector import StopSignDetector
from car_communication.abstract_communication import AbstractCommunication
from car_communication.can_bus_communication import CanBusCommunication
from car_communication.car_serial_communication import CarSerialCommunication
from car_communication.car_stepper_communication import CarStepperCommunication

from qr_code.qr_code import QRCode

class Headless():  # pylint: disable=R0903
    '''Class handling headless running'''
    # pylint: disable=R0902
    def __init__(self, conf: dict): # pylint: disable=R0912
        self.state = States.WAITING  # Start in "idle" state
        self.car_comm: AbstractCommunication
        # pylint: disable=R0903
        if conf["car_comm_interface"] == "serial":
            self.car_comm = CarSerialCommunication(conf["serial"])
        elif conf["car_comm_interface"] == "can":
            self.car_comm = CanBusCommunication(conf["can"])
        elif conf["car_comm_interface"] == "stepper":
            self.car_comm = CarStepperCommunication(conf["stepper"])

        # Network config for main connection + camera(s)
        self.net_main = NetworkSettings(conf["network"]["host"], conf["network"]["port"])
        self.net_cam0 = NetworkSettings(conf["network"]["host"], conf["network"]["port_cam0"])
        self.net_cam1 = NetworkSettings(conf["network"]["host"], conf["network"]["port_cam1"])

        # Start main socket server for connections
        self.socket_server = MultiSocketServer(self.net_main)
        self.socket_server.start()

        self.camera_missing_frame = 0

        self.cam0_stream = CamSocketStream(self.net_cam0)
        if conf["network"]["stream_en_cam0"] is True:
            print("Starting camera stream")
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
        self.stop_sign_detector = StopSignDetector('stop_sign_model.xml')

        while True:
            # Check and handle incoming data
            for data in self.socket_server:
                print (data)
                if MessageId(data[0]) is MessageId.CMD_SET_STATE:
                    self.state = data[1]
                    print("State changed to: ")
                    print(States(data[1]).name)
                if MessageId(data[0]) is MessageId.CMD_JOYSTICK_DIRECTIONS:
                    pass
                    # Handle joystick directions

            # Take new picture, handle socket transfers
            ret, frame0 = self.cam0_handler.get_cv_frame()

            if ret is True:
                self.camera_missing_frame = 0
                self.cam0_stream.send_to_all(frame0)
                self.cam1_stream.send_to_all(frame0)
            else:
                self.camera_missing_frame += 1
                print(f"Could not get frame from camera: {self.cam0_handler.camera_id}!")
                if self.camera_missing_frame > 10:
                    print("Exceeded number of missing frames in a row. Stopping headless.")
                    print(self.cam0_handler.refresh_camera_list())
                    break

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
                if current_qr_data['distances'] is not None and \
                        len(current_qr_data['distances']) > 0:
                    print(output_data)
                if len(current_stop_sign) > 0:
                    print(current_stop_sign)

            elif self.state is States.PARKING:
                pass
            elif self.state is States.DRIVING:
                # example:
                self.car_comm.set_motor_speed(1, 100, 1, 100)
