'''camera_handler.py: DATBAC23 camera functionality library'''
__copyright__ = 'Copyright 2023, DATBAC23'
__license__ = 'Apache-2.0'
__version__ = '0.1.0'
__status__ = 'Testing'
from typing import List
import cv2

class CameraHandler:
    '''Camera functionality'''
    def __init__(self, camera_id: int = 999 ):
        '''Initialize an empty list of cameras'''
        self.available_camera_list = []
        if camera_id != 999:
            self.cv_camera = cv2.VideoCapture(camera_id)

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
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
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

    def get_cv_frame(self):
        '''Returns a new CV frame'''
        if self.cv_camera is not None:
            return self.cv_camera.read()
        return None

# pylint: disable=R0902
if __name__ == '__main__':
    camera_handler = CameraHandler()
    cameras = camera_handler.refresh_camera_list()
    for cam in cameras:
        print(cam)
