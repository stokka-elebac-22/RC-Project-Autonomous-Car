'''DOC'''
import cv2

if __name__ == '__main__':
    DIRECTORY = 'tests/images/parking_slot_detection_2/'
    cam = cv2.VideoCapture(1)

    COUNT = 0
    while True:
        frames = []
        RETS = True
        ret, frame = cam.read()
        cv2.imshow('cam', frame)
        frames.append((frame, cam))

        if cv2.waitKey(1) & 0xFF == ord('s'): # stop loop by pressing s
            print('Stopping...')
            break

        if not RETS:
            continue

        if cv2.waitKey(1) & 0xFF == ord('c'):
            print('Capturing...')
            for frame, title in frames:
                cv2.imwrite(f'{DIRECTORY}/{title}_{COUNT}.jpg', frame)
            COUNT += 1
