import cv2 as cv

"""
Assuming you take photos with two camera at the same time.
It will work with one camera, but it will end up in the calibrate left directory
"""

if __name__ == '__main__':
    DIRECTORY = 'tests/images/qr_code/distance'
    CAMERA_ID_LEFT = 1
    CAMERA_ID_RIGHT = 2
    BOARD_DIMENSIONS = (8, 6)
    cam1 = cv.VideoCapture(CAMERA_ID_LEFT)
    cam2 = cv.VideoCapture(CAMERA_ID_RIGHT)
    # cameras = [(cam1, 'left'), (cam2, 'right')]
    cameras = [(cam1, 'left')]

    qcd = cv.QRCodeDetector()

    trigger = False
    count = 0
    while True:
        frames = []
        rets = True
        for cam in cameras:
            ret, frame = cam[0].read()
            cv.imshow(cam[1], frame)
            if not ret:
                rets = False
                break
            frames.append((frame, cam[1]))

        if cv.waitKey(1) & 0xFF == ord('s'): # stop loop by pressing s
            print('Stopping...')
            break

        if cv.waitKey(1) & 0xFF == ord('c'):
            print('Capturing...')
            trigger = True

        if not rets:
            continue

        for frame in frames:
            ret, _, _, _ = qcd.detectAndDecodeMulti(frame[0])
            if not ret:
                rets = False
                break
        if not rets:
            continue

        if trigger:
            print('Done\n')
            for frame, title in frames:
                cv.imwrite(f'{DIRECTORY}/{title}/{title}_{count}.jpg', frame)
            count += 1
            trigger = False
