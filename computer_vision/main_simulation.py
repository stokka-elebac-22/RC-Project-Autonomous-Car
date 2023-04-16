'''
The main file for the driving simulation
'''
import os
import sys
import yaml
from pynput import keyboard
from driving.driving_states import DrivingStates
from simulation.simulation_action import SimulationAction
from camera_handler.camera_handler import CameraHandler
from camera_handler.camera import Camera
from module_setup import ModuleSetup

class Simulation: # pylint: disable=R0903
    '''
    The class for starting init
    '''
    def __init__(self, conf: dict, module_setup: ModuleSetup) -> None:
        self.conf = conf
        self.cam = None
        self.cam0_stream = None
        self.cam1_stream = None
        if self.conf['simulation']['live']:
            self.cam = self.__camera_setup()
        
        print('Initializing the modules')
        pathfinding = module_setup.pathfinding_setup()
        qr_code = module_setup.qr_code_setup()
        parking_slot_detector = module_setup.parking_slot_detector_setup()
        lane_detector = module_setup.lane_detector_setup()
        traffic_sign_detector = module_setup.traffic_sign_detector_setup()

        # ----- DRIVING ----- #
        driving = DrivingStates(
            conf=conf,
            pathfinding=pathfinding,
            qr_code=qr_code,
            parking_slot_detector=parking_slot_detector,
            lane_detector=lane_detector,
            stop_sign_detector=traffic_sign_detector)
        
        self.driving_setup = SimulationAction(
            conf=conf,
            driving=driving,
            camera=self.cam)
        self.run()

    def __camera_setup(self):
        # ----- CAMERAS ----- #
        print('Setting up cameras...')
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
        ret, _ = cam.read()
        if not ret:
            raise ConnectionError
        return cam

    def run(self):
        '''Run the simulation'''
        print('Running...')
        self.driving_setup.run()


if __name__ == '__main__':
    CONFIG_FILE = 'config'
    print('Reading configuration file...')
    # ----- CONFIG ----- #
    with open(CONFIG_FILE + '.yml', 'r', encoding='utf8') as f:
        try:
            c = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

    # ----- TEST IF PATHS ARE CORRECT ----- #
    if c['simulation']['active']:
        image_paths = c['simulation']['image_paths']
        for image_path in [image_paths['camera_view'], image_paths['arrow']]:
            if not os.path.exists(image_path):
                raise FileNotFoundError

    # ----- INTERRUPTS ----- #
    def on_press(key):
        '''on_press'''
        if key == keyboard.Key.esc:
            sys.exit()

    # Collect events until released
    listener = keyboard.Listener(
        on_press=on_press
    )
    listener.start()


    simulation = Simulation(c, ModuleSetup(c))
    simulation.run()
