import cv2 as cv
from camera import Camera

DIRECTORY = 'images/'

cam1 = Camera(0, 'left')
cam2 = Camera(2, 'right')
cameras: Camera = [cam1, cam2]

count = 0
while True:
    frames = []
    for cam in cameras:
        ret, frame = cam.read()
        frames.append((frame, cam.window_name))
        cv.imshow(cam.winodw_name, frame)
    
    if cv.waitKey(1) & 0xFF == ord('c'): # capture frame by pressing c
        for frame in frames:
            cv.imwrite(f'{DIRECTORY}{frame[1]}_{count}.jpg', frame[0])
        count += 1

    if cv.waitKey(1) & 0xFF == ord('s'): # stop loop by pressing s
        break

for cam in cameras:
    cam.cap.release()