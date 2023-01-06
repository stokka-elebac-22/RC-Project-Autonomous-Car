from qr_code import QRCode
from camera import Camera

# ----- ORIGINAL MEASUREMENTS -----
# QR Code measured, 55mm lense
QR_SIZE_PX = 1500
QR_SIZE_MM = 179
QR_DISTANCE = 1000

if "__main__" == __name__:
    qr_code = QRCode(QR_SIZE_PX, QR_SIZE_MM, QR_DISTANCE) 
    camera = Camera(qr_code) 
    camera.run()