'''DOC'''
import cv2 as cv
from qr_code import QRCode

if __name__ == '__main__':
    DIRECTORY = 'tests/images/qr_code/webcam'
    CAMERA_ID_LEFT = 0
    CAMERA_ID_RIGHT = 2
    cam1 = cv.VideoCapture(CAMERA_ID_LEFT)
    cam2 = cv.VideoCapture(CAMERA_ID_RIGHT)
    cameras = [(cam1, 'distance')]

    QR_SIZE_PX = 76
    QR_SIZE_MM = 52
    QR_DISTANCE = 500

    qr_code = QRCode(QR_SIZE_PX, QR_SIZE_MM, QR_DISTANCE)

    TRIGGER = False
    COUNT = 0
    while True:
        frames = []
        RETS = True
        for cam in cameras:
            ret, frame = cam[0].read()
            retval, distances, angles, points, _ = qr_code.get_data(frame)
            qr_code.display(frame, verbose=2)
            if not all(ret):
                RETS = False
                break
            frames.append((frame, cam[1]))

        if cv.waitKey(1) & 0xFF == ord('s'): # stop loop by pressing s
            print('Stopping...')
            break

        if cv.waitKey(1) & 0xFF == ord('c'):
            print('Capturing...')
            TRIGGER = True

        if TRIGGER:
            if not RETS:
                continue

            print('Done\n')
            for frame, title in frames:
                cv.imwrite(f'{DIRECTORY}/{title}/{title}_{COUNT}.jpg', frame)
            COUNT += 1
            TRIGGER = False
