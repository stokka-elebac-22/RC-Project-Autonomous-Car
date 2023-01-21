import cv2 as cv

"""
Assuming you take photos with two camera at the same time.
It will work with one camera, but it will end up in the calibrate left directory
"""

if __name__ == '__main__':
    DIRECTORY = 'tests/images/qr_code'
    CAMERA_ID_LEFT = 1
    CAMERA_ID_RIGHT = 2
    BOARD_DIMENSIONS = (8, 6)
    cam1 = cv.VideoCapture(CAMERA_ID_LEFT)
    cam2 = cv.VideoCapture(CAMERA_ID_RIGHT)
    cameras = [(cam1, 'left'), (cam2, 'right')]

    count = 0
    trigger = False
    while True:
        if cv.waitKey(1) & 0xFF == ord('c'):
            print('Capturing...')
            trigger = True

        if trigger is False:
            continue

        frames = []
        rets = True
        for cam in cameras:
            ret, frame = cam.read()
            if not ret:
                rets = False
                break
            gray = cv.cvtColor(cam[0], cv.COLOR_BGR2GRAY)
            frames.append((frame, cam[1]))
            ret, _ = cv.findChessboardCorners(gray, BOARD_DIMENSIONS, None)
            if not ret:
                rets = False
                break
            cv.imshow(cam[1], cam[0])
        if not rets:
            continue

        print('Done\n')
        for i, frame in enumerate(frames):
            cv.imwrite(f'{DIRECTORY}/{cameras[i][1]}/{frame[1]}_{count}.jpg', frame[0])
        trigger = False
        count += 1

        if cv.waitKey(1) & 0xFF == ord('s'): # stop loop by pressing s
            break


