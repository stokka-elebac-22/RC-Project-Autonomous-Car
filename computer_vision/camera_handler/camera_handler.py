"""camera_handler.py: DATBAC23 camera functionality library"""
__copyright__ = "Copyright 2023, DATBAC23"
__license__ = "Apache-2.0"
__version__ = "0.1.0"
__status__ = "Testing"
from PyQt6.QtGui import QPixmap, QColor, QImage
from PyQt6.QtCore import Qt
import cv2

class CameraHandler:
    """Camera functionality"""
    def __init__(self):
        """Initialize an empty list of cameras"""
        self.available_camera_list = []

    def get_camera_string(self, id: int) -> str:
        """Return a string describing camera with id"""
        return "Cam" + str(self.available_camera_list[id]["id"]) + ": " \
            + str(self.available_camera_list[id]["res_w"]) + "x" \
            + str(self.available_camera_list[id]["res_h"]) \
            + " (" + str(self.available_camera_list[id]["fps"]) + "fps)"

    def get_camera_list(self):
        """Return the list of cameras"""
        return self.available_camera_list

    def refresh_camera_list(self):
        """Test camera input to create a list of available cameras"""
        index = 0
        testing = 1
        arr = []
        while testing:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                testing = 0
            else:
                camera = {}
                camera["id"] = index
                camera["res_w"] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                camera["res_h"] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                camera["fps"] = int(cap.get(cv2.CAP_PROP_FPS))
                arr.append(camera)
            cap.release()
            index += 1
        self.available_camera_list = arr
        return arr

    def convert_cv_qt(self, cv_img, w, h):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)

if __name__ == "__main__":
    camera_handler = CameraHandler()
    cameras = camera_handler.refresh_camera_list()
    for camera in cameras:
        print(camera)
