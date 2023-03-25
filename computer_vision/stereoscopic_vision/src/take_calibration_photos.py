'''DOC'''
import time
import cv2 as cv
from camera import Camera

if __name__ == '__main__':
    DIRECTORY = 'computer_vision/stereoscopic_vision/images/test_imagestest'
    CAMERA_ID_LEFT = 1
    CAMERA_ID_RIGHT = 2
    BOARD_DIMENSIONS = (13, 9)
    cam_left = Camera(CAMERA_ID_LEFT)
    cam_right = Camera(CAMERA_ID_RIGHT)
    cameras = [(cam_left, 'left'), (cam_right, 'right')]

    # check if all cameras work
    for cam in cameras:
        ret, _ = cam[0].read()
        if not ret:
            print(f'{cam[1]} camera could not connect...')
            raise ConnectionError

    qcd = cv.QRCodeDetector()

    TRIGGER = False
    COUNT = 0

    start_time = time.time()

    TIME_TH = 5 # 2 seconds between each photo

    while True:
        frames = []
        RETS = True
        for cam in cameras:
            ret, frame = cam[0].read()
            if not ret:
                RETS = False
                break
            cv.imshow(cam[1], frame)
            frames.append((frame, cam[1]))

        if cv.waitKey(1) & 0xFF == ord('s'): # stop loop by pressing s
            print('Stopping...')
            break

        cur_time = time.time()
        ts = cur_time - start_time
        if ts >= TIME_TH and TRIGGER is False:
            print('Capturing...')
            TRIGGER = True

        if TRIGGER:
            if not RETS:
                continue
            for frame, _ in frames:
                gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                ret, _ = cv.findChessboardCorners(gray, BOARD_DIMENSIONS, None)
                if not ret:
                    RETS = False
                    break
            if not RETS:
                continue

            print('Done\n')
            for frame, title in frames:
                cv.imwrite(f'{DIRECTORY}/{title}_{COUNT}.jpg', frame)
            COUNT += 1
            TRIGGER = False

            start_time = time.time()
