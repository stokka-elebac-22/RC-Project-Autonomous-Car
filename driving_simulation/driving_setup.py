'''The script for the driving loop'''
import os
import sys
from typing import List
import cv2 as cv
from driving import Driving
from defines import States
from defines import ActionsDict
# from pynput import keyboard
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from driving_simulation.lib import rotate_image # pylint: disable=C0413
from computer_vision.camera_handler.camera import Camera # pylint: disable=C0413

class DrivingSetup:
    '''The loop for driving'''
    def __init__(self, conf: dict, driving: Driving, camera: Camera, image_paths: dict):
        self.conf = conf
        self.driving = driving
        self.camera = camera
        self.image_paths = image_paths

        # STATES:
        self.state = States.DRIVING

        # ----- INTERRUPTS ----- #
        self.running = True
        # self.__interrupts()

    def __interrupts(self):
        pass
        # def on_press(key):
        #     if key == keyboard.Key.esc:
        #         # Stop listener
        #         self.running = False
        #         return False
        #     return True

        # # Collect events until released
        # with keyboard.Listener(
        #         on_press=on_press) as listener:
        #     listener.join()

    def run(self):
        '''Method for running'''
        while self.running:
            actions = self.next()
            self.display(actions)
        print('Stopping...')

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
            cv.waitKey()
        else:
            print(f'Path does not exists {self.image_paths["arrow"]}')
