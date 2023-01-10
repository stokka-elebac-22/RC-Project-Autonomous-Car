from camera import Camera
from stereoscopic_vision import StereoscopicVision

# ----- ORIGINAL MEASUREMENTS -----
# QR Code measured, 55mm lense
QR_SIZE_PX = 76
QR_SIZE_MM = 52
QR_DISTANCE = 500 

if "__main__" == __name__:
    '''
    NOTE: if you also have a webcam (that you do not want to use), use id 0 and 2
    '''
    cam1 = Camera(camera_id=0, window_name='Camera 1') 
    cam2 = Camera(camera_id=2, window_name='Camera 2')
    stereo_vision = StereoscopicVision(cam1, cam2)
    stereo_vision.run()