'''DOC'''
import cv2 as cv

if __name__ == '__main__':
    DIRECTORY = 'computer_vision/stereoscopic_vision/images/calibrate_large/'
    CAMERA_ID_LEFT = 1
    CAMERA_ID_RIGHT = 0
    BOARD_DIMENSIONS = (8, 6)
    cam1 = cv.VideoCapture(CAMERA_ID_LEFT)
    cam2 = cv.VideoCapture(CAMERA_ID_RIGHT)
    cameras = [(cam1, 'left'), (cam2, 'right')]

    qcd = cv.QRCodeDetector()

    TRIGGER = False
    COUNT = 0
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

        if cv.waitKey(1) & 0xFF == ord('c'):
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
                cv.imwrite(f'{DIRECTORY}/{title}/{title}_{COUNT}.jpg', frame)
            COUNT += 1
            TRIGGER = False
