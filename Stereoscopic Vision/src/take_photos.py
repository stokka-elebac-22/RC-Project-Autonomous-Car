import cv2 as cv
from camera import Camera

DIRECTORY = 'Stereoscopic Vision/images/'

cam1 = Camera(0, 'left')
cam2 = Camera(2, 'right')
cameras: Camera = [cam1, cam2]

count = 0
while True:
    frames = []
    for cam in cameras:
        ret, frame = cam.read()
        if not ret:
            print('Error: Could not return the frame')
            continue
        frames.append((frame, cam.window_name))
        cv.imshow(cam.window_name, frame)
    
    if cv.waitKey(1) & 0xFF == ord('c'): # capture frame by pressing c
        print('Capturing...')
        for frame in frames:
            cv.imwrite(f'{DIRECTORY}{frame[1]}_{count}.jpg', frame[0])
        count += 1

    if cv.waitKey(1) & 0xFF == ord('s'): # stop loop by pressing s
        break

for cam in cameras:
    cam.cap.release()