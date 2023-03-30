'''The script for the driving loop'''
import os
import sys
from typing import List
import cv2 as cv
from defines import States
from defines import ActionsDict
from pynput import keyboard
try:
    from computer_vision.simulation.driving import Driving
    from computer_vision.camera_handler.camera import Camera
    from computer_vision.camera_handler.lib import rotate_image
except ImportError:
    from driving import Driving
    from camera_handler.camera import Camera
    from camera_handler.lib import rotate_image

class DrivingSetup:
    '''The loop for driving'''
    def __init__(self, conf: dict, driving: Driving, camera: Camera=None):
        self.conf = conf
        self.driving = driving
        self.camera = camera
        self.image_paths = self.conf['simulation']['image_paths']

        # STATES:
        self.state = States.DRIVING

        # ----- ACTIONS ----- #
        self.actions = None

        # ----- INIT ACTIONS ----- #
        if self.conf['simulation']['live'] is False:
            self.__init_actions()

        # ----- INTERRUPTS ----- #
        self.running = True
        self.__interrupts()

    def __interrupts(self):
        def on_press(key):
            if key == keyboard.Key.esc:
                self.running = False
                return False
            return True

        # Collect events until released
        listener = keyboard.Listener(
            on_press=on_press
        )
        listener.start()

    def __init_actions(self):
        frame = self.conf['simulation']['image_paths']['camera_view']
        height, width, _ = frame.shape
        self.actions = self.driving.driving(frame, (width, height))

    def run(self):
        '''Method for running'''
        while self.running:
            if self.conf['simulation']['live']:
                actions = self.next() # pylint: disable=E1102
                if actions is not None:
                    self.actions = actions
            self.display(self.actions)
        print('Stopping...')
        sys.exit()

    def next(self) -> List[ActionsDict]:
        '''The next iteration in the loop'''
        ret, frame = self.camera.read()
        if not ret:
            return None
        if self.state == States.DRIVING:
            actions: List[ActionsDict] = self.driving.driving(frame, self.camera.get_dimensions())
        return actions

    def display(self, action: ActionsDict):
        '''Display the arrow or other symbols'''
        if os.path.exists(self.image_paths['arrow']):
            img = cv.imread(self.image_paths['arrow'])
            # rotate image
            if action is not None:
                img = rotate_image(img, action['angles'][0])
            cv.imshow('', img)
            cv.waitKey(1)
        else:
            print(f'Path does not exists: {self.image_paths["arrow"]}')
            raise FileNotFoundError
