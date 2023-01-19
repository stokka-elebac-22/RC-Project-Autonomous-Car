"""MAIN"""
from camera import Camera

# ----- ORIGINAL MEASUREMENTS -----
# QR Code measured, 55mm lense
QR_SIZE_PX = 76
QR_SIZE_MM = 52
QR_DISTANCE = 500

if "__main__" == __name__:
    camera = Camera()
    camera.run(verbose=2)
