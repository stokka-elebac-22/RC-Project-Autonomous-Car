'''DOC'''
import cv2 as cv

if __name__ == '__main__':
    DIRECTORY = 'tests/images/distance'
    CAMERA_ID = 1
    cam = cv.VideoCapture(CAMERA_ID)

    TRIGGER = False
    COUNT = 0
    while True:
        ret, frame = cam.read()
        if not ret:
            continue
        cv.imshow('frame', frame)

        if cv.waitKey(1) & 0xFF == ord('s'): # stop loop by pressing s
            print('Stopping...')
            break

        if cv.waitKey(1) & 0xFF == ord('c'):
            print('Taking picture...')
            cv.imwrite(f'{DIRECTORY}/frame_{COUNT}.jpg', frame)
            COUNT += 1
