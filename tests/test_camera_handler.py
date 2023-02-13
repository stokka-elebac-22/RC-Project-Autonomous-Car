'''test_qr_code.py'''
from computer_vision.camera_handler.camera_handler import CameraHandler

def test_refresh_camera_list():
    '''This method should be tested manually with a camera attached'''
    assert True

def test_get_camera_list():
    '''Test method that returns the list of detected cameras'''
    camera_handler = CameraHandler()
    camera_list =  [
            { 'id': 0, 'res_w' : 640 , 'res_h' : 480, 'fps': 30},
            { 'id': 1, 'res_w' : 1024 , 'res_h' : 768, 'fps': 30},
    ]
    camera_handler.available_camera_list = camera_list
    assert camera_handler.get_camera_list() == camera_list

def test_get_camera_string():
    '''Test if correct string is returned for a camera'''
    camera_handler = CameraHandler()
    camera_handler.available_camera_list = [
            { 'id': 0, 'res_w' : 640 , 'res_h' : 480, 'fps': 30},
            { 'id': 1, 'res_w' : 1024 , 'res_h' : 768, 'fps': 30},
        ]
    assert camera_handler.get_camera_string(0) == 'Cam0: 640x480 (30fps)'
    assert camera_handler.get_camera_string(1) == 'Cam1: 1024x768 (30fps)'
