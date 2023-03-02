'''DOC'''
import cv2 as cv

if __name__ == '__main__':
    DIRECTORY = 'tests/images/stereoscopic_vision/test/11'
    CAMERA_ID_LEFT = 1
    CAMERA_ID_RIGHT = 0
    cam1 = cv.VideoCapture(CAMERA_ID_LEFT)
    cam2 = cv.VideoCapture(CAMERA_ID_RIGHT)
    cameras = [(cam1, 'left'), (cam2, 'right')]

    qcd = cv.QRCodeDetector()

    COUNT = 7
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

        if not RETS:
            continue

        if cv.waitKey(1) & 0xFF == ord('c'):
            print('Capturing...')
            for frame, title in frames:
                cv.imwrite(f'{DIRECTORY}/{title}/{title}_{COUNT}.jpg', frame)
            COUNT += 1
