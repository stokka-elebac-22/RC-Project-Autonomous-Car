'''The script for the driving loop'''
from pynput import keyboard
try:
    from computer_vision.simulation.driving import Driving
    from computer_vision.camera_handler.camera import Camera
except ImportError:
    import os
    import sys
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)
    from simulation.driving import Driving
    from camera_handler.camera import Camera

class DrivingSetup:
    '''The loop for driving'''
    def __init__(self, conf: dict, driving: Driving, camera: Camera):
        self.conf = conf
        self.driving = driving
        self.camera = camera

        # ----- INTERRUPTS ----- #
        self.running = True
        self.__interrupts()

    def __interrupts(self):
        def on_press(key):
            if key == keyboard.Key.esc:
                # Stop listener
                self.running = False
                return False
            return True

        # Collect events until released
        with keyboard.Listener(
                on_press=on_press) as listener:
            listener.join()

    def run(self):
        '''Method for running'''
        while self.running:
            self.__next()
        print('Stopping...')

    def next(self):
        '''The next iteration in the loop'''
