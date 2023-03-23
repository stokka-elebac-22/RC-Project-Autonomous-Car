'''
The main file for the driving simulation
'''
import yaml
from driving import Driving
from driving_setup import DrivingSetup
from computer_vision.camera_handler.camera_handler import CameraHandler
from computer_vision.camera_handler.camera import Camera

CONFIG_FILE = 'driving_simulation/config'

if __name__ == '__main__':
    # ----- CONFIG ----- #
    with open(CONFIG_FILE + '.yml', 'r', encoding='utf8') as f:
        try:
            conf = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

    # ----- CAMERAS ----- #
    camera_handler = CameraHandler()
    cameras = camera_handler.refresh_camera_list()
    # finding the resolution
    RESOLUTION = None
    if conf['camera']['active'] == 'web':
        RESOLUTION = conf['camera']['camera_resolution']['web']
    elif conf['camera']['active'] == 'logi':
        RESOLUTION = conf['camera']['camera_resolution']['logi']

    if RESOLUTION is None:
        cam = Camera(cameras[0]['id'])
    else:
        cam = Camera(cameras[0]['id'], RESOLUTION)
    driving = Driving()
    driving_setup = DrivingSetup(conf=conf, driving=driving, camera=cam)
    driving_setup.run()
