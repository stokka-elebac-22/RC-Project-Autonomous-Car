from qr_code import QRCode
from camera import Camera

# ----- ORIGINAL MEASUREMENTS -----
# QR Code measured, 55mm lense
QR_SIZE_PX = 76
QR_SIZE_MM = 52
QR_DISTANCE = 500 

if "__main__" == __name__:
    qr_code = QRCode(QR_SIZE_PX, QR_SIZE_MM, QR_DISTANCE, values_length=20) 
    camera = Camera(qr_code) 
    camera.run(verbose=2)