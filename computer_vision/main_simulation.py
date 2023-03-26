'''
The main file for the driving simulation
'''
import yaml
from simulation.driving import Driving
from simulation.driving_setup import DrivingSetup
try:
    from computer_vision.camera_handler.camera_handler import CameraHandler
    from computer_vision.camera_handler.camera import Camera
except ImportError:
    from camera_handler.camera_handler import CameraHandler
    from camera_handler.camera import Camera



class Simulation:
    '''
    The class for running the simulation
    '''
    def __init__(self, conf: dict) -> None:
        self.conf = conf
        cam = self.__camera_setup()
        self.driving = Driving()
        self.driving_setup = DrivingSetup(conf=conf, driving=self.driving, camera=cam)

    def __camera_setup(self):
        # ----- CAMERAS ----- #
        camera_handler = CameraHandler()
        cameras = camera_handler.refresh_camera_list()
        # finding the resolution
        resolution = None
        if self.conf['camera']['active'] == 'web':
            resolution = self.conf['camera']['camera_resolution']['web']
        elif self.conf['camera']['active'] == 'logi':
            resolution = self.conf['camera']['camera_resolution']['logi']

        if resolution is None:
            cam = Camera(cameras[0]['id'])
        else:
            cam = Camera(cameras[0]['id'], resolution)
        return cam

    def run(self):
        '''Run the simulation'''
        self.driving_setup.run()


if __name__ == '__main__':
    CONFIG_FILE = 'config'
    # ----- CONFIG ----- #
    with open(CONFIG_FILE + '.yml', 'r', encoding='utf8') as f:
        try:
            c = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

    simulation = Simulation(c)
    simulation.run()
