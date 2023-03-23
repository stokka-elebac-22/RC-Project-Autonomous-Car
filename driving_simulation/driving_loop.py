'''The script for the driving loop'''
from driving import Driving
from pynput import keyboard

class DrivingLoop:
    '''The loop for driving'''
    def __init__(self, driving: Driving):
        self.driving = driving

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
        while self.end:
            next()

    def next(self):
        '''The next iteration in the loop'''
