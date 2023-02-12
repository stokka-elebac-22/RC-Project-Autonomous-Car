'''camera_handler.py: DATBAC23 camera functionality library'''
__copyright__ = 'Copyright 2023, DATBAC23'
__license__ = 'Apache-2.0'
__version__ = '0.1.0'
__status__ = 'Testing'
from typing import List
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import pyqtSignal, Qt, QThread
import cv2
import numpy as np

class CameraHandler:
    '''Camera functionality'''
    def __init__(self):
        '''Initialize an empty list of cameras'''
        self.available_camera_list = []

    def get_camera_string(self, camera_id: int) -> str:
        '''Return a string describing camera with id'''
        return 'Cam' + str(self.available_camera_list[camera_id]['id']) + ': ' \
            + str(self.available_camera_list[camera_id]['res_w']) + 'x' \
            + str(self.available_camera_list[camera_id]['res_h']) \
            + ' (' + str(self.available_camera_list[camera_id]['fps']) + 'fps)'

    def get_camera_list(self) -> List[dict]:
        '''Return the list of cameras'''
        return self.available_camera_list

    def refresh_camera_list(self) -> List[dict]:
        '''Test camera input to create a list of available cameras'''
        index = 0
        testing = 1
        arr = []
        while testing:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                testing = 0
            else:
                camera = {}
                camera['id'] = index
                camera['res_w'] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                camera['res_h'] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                camera['fps'] = int(cap.get(cv2.CAP_PROP_FPS))
                arr.append(camera)
            cap.release()
            index += 1
        self.available_camera_list = arr
        return arr

def get_cv_frame(cam_id: int):
    '''Returns a new CV frame'''
    print(cam_id)

def convert_cv_qt(cv_img, scale_w: int, scale_h: int) -> QPixmap:
    '''Convert from an opencv image to QPixmap'''
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    # pylint: disable=C0103
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QImage(
        rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
    p = convert_to_Qt_format.scaled(scale_w, scale_h, Qt.AspectRatioMode.KeepAspectRatio)
    return QPixmap.fromImage(p)

class VideoThread(QThread):
    '''Video Thread'''
    change_pixmap_signal = pyqtSignal(np.ndarray)
    camera_id = 0

    def __init__(self, camera_id: int):
        super().__init__()
        self._run_flag = True
        self.camera_id = camera_id

    def run(self):
        '''Run'''
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        '''Sets run flag to False and waits for thread to finish'''
        self._run_flag = False
        self.wait()

if __name__ == '__main__':
    camera_handler = CameraHandler()
    cameras = camera_handler.refresh_camera_list()
    for cam in cameras:
        print(cam)
