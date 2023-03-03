'''DOC'''
import cv2 as cv
from pynput import keyboard

if __name__ == '__main__':
    DIRECTORY = 'computer_vision/stereoscopic_vision/images'
    CAMERA_ID_LEFT = 1
    CAMERA_ID_RIGHT = 0
    BOARD_DIMENSIONS = (8, 6)
    print('Setting up cameras...')
    cam1 = cv.VideoCapture(CAMERA_ID_LEFT)
    cam2 = cv.VideoCapture(CAMERA_ID_RIGHT)
    print('Done\n')
    cameras = [(cam1, 'left'), (cam2, 'right')]
    cameras = []

    qcd = cv.QRCodeDetector()

    TRIGGER = False
    COUNT = 0

    RUN = True

    def on_press(key):
        '''Press'''
        print('Capturing...')
        global TRIGGER # pylint: disable=W0603
        if key == keyboard.Key.space:
            TRIGGER = True

    def on_release(key):
        '''Release'''
        global RUN # pylint: disable=W0603
        if key == keyboard.Key.esc:
            # Stop listener
            RUN = False

    print('Setting up listeners...')
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()  # start to listen on a separate thread
    # listener.join()  # remove if main thread is polling self.keys
    print('Done\n')

    while RUN:
        frames = []
        RETS = True
        for cam in cameras:
            ret, frame = cam[0].read()
            if not ret:
                RETS = False
                break
            cv.imshow(cam[1], frame)
            frames.append((frame, cam[1]))

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
