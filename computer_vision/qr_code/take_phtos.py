import cv2 as cv

"""
DOC
"""

if __name__ == '__main__':
    DIRECTORY = 'tests/images/qr_code/webcam'
    CAMERA_ID_LEFT = 0
    CAMERA_ID_RIGHT = 2
    cam1 = cv.VideoCapture(CAMERA_ID_LEFT)
    cam2 = cv.VideoCapture(CAMERA_ID_RIGHT)
    cameras = [(cam1, 'distance')]

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

        if trigger:
            if not rets:
                continue

            for frame in frames:
                ret, _, _, _ = qcd.detectAndDecodeMulti(frame[0])
                if not ret:
                    rets = False
                    break
            if not rets:
                continue

            print('Done\n')
            for frame, title in frames:
                cv.imwrite(f'{DIRECTORY}/{title}/{title}_{count}.jpg', frame)
            count += 1
            trigger = False
