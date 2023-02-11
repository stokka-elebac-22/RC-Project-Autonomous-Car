'''
The main file for the driving logic.
This file should only contain short code
'''
from computer_vision.qr_code.qr_code import QRCode
from computer_vision.environment.src.environment import Environment

# ---------- CONSTANTS ---------- #

# ---------- MAIN ---------- #
if __name__ == '__main__':
    # ---------- INIT ---------- #
    ### init camera ###
    ### init qr code ###
    QR_CODE_SIZE_PX = 76
    QR_CODE_SIZE_MM = 52
    QR_CODE_DISTANCE = 500
    qr_code = QRCode(QR_CODE_SIZE_PX, QR_CODE_SIZE_MM, QR_CODE_DISTANCE)
    ### init environment ###
    SIZE = (10, 11)
    WINDOW_WIDTH = 600
    WINDOW_SIZE = (WINDOW_WIDTH* (SIZE[1]/SIZE[0]), WINDOW_WIDTH)
    env= Environment(SIZE, 1, {'object_id': 10})

    # ---------- LOOP ---------- #
    while True:
        # ---------- GET CAMERA INFORMATION---------- #
        ### QR Code ###
        # qr_code.get_data(frame)

        ### Line detection ###

        # ---------- UPDATE ENVIRONMENT ---------- #

        # ---------- ACTION ---------- #
        pass
