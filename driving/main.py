'''
The main file for the driving logic.
This file should only contain short code
'''
from computer_vision.qr_code.qr_code import QRCode
from computer_vision.environment.src.environment import Environment
from computer_vision.traffic_sign_detection.main import TrafficSignDetector
from computer_vision.line_detection.parking_slot_detection import ParkingSlotDetector

# ---------- CONSTANTS ---------- #

# ---------- MAIN ---------- #
if __name__ == '__main__':
    # ---------- INIT ---------- #
    ### init camera ###
    ### init qr code ###
    qr_size = {
        'px': 76,
        'mm': 52,
        'distance': 500
    }
    qr_code = QRCode(qr_size)

    ### init traffic sign detector ###
    sign_size = {
        'px': 10,
        'mm': 61,
        'distance': 200
    }
    traffic_sign_detection = TrafficSignDetector(size=sign_size)

    ### init lane detector ###

    ### init parking slot detector ###
    parking_slot_detector = ParkingSlotDetector(
        hough=[200, 5], iterations=[5, 2])

    ### init environment ###
    SIZE = (10, 11)
    WINDOW_WIDTH = 600
    WINDOW_SIZE = (WINDOW_WIDTH* (SIZE[1]/SIZE[0]), WINDOW_WIDTH)
    env= Environment(SIZE, 1, {'object_id': 10})

    # ---------- LOOP ---------- #
    while True:
        # ---------- GET CAMERA INFORMATION---------- #
        ### QR Code ###
        # data = qr_code.get_data(frame)

        ### Line detection ###

        ### Trafic Sign Detection ###
        # output_signs = traffic_sign_detection.detect_signs(frame)
        # traffic_sign_detection.show_signs(frame, output_signs)

        ### Lane Detection ###

        ### Parking Slot Detection ###
        # parking_lines = parking_slot_detector.detect_parking_lines(frame, data)
        # parking_lines.append(
        #     parking_slot_detector.get_closing_line_of_two_lines(parking_lines))
        # parking_slot_detector.show_lines(frame, parking_lines)


        # ---------- UPDATE ENVIRONMENT ---------- #

        # ---------- ACTION ---------- #
        pass
