'''
The main file for the driving simulation
'''
import yaml
from driving import Driving
from driving_setup import DrivingSetup
from computer_vision.camera_handler.camera_handler import CameraHandler
from computer_vision.camera_handler.camera import Camera

CONFIG_FILE = 'config'

if __name__ == '__main__':
    # ----- CONFIG ----- #
    with open(CONFIG_FILE + '.yml', 'r', encoding='utf8') as f:
        try:
            config_file = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

    camera_handler = CameraHandler()
    cameras = camera_handler.refresh_camera_list()
    cam = Camera(cameras[0]['id'])
    print(cameras)
    driving = Driving()
    driving_setup = DrivingSetup(conf=config_file, driving=driving, camera=cam)
    driving_setup.run()
