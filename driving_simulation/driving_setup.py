'''The script for the driving loop'''
import os
import sys
import cv2 as cv
from driving import Driving
from defines import States
# from pynput import keyboard
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
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
        self.__interrupts()

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
            self.next()
            self.display()
        print('Stopping...')

    def next(self):
        '''The next iteration in the loop'''

    def display(self):
        '''Display the arrow or other symbols'''
        if os.path.exists(self.image_paths['arrow']):
            img = cv.imread(self.image_paths['arrow'])
            cv.imshow('', img)
            cv.waitKey(0)
        else:
            print(f'Path does not exists {self.image_paths["arrow"]}')
