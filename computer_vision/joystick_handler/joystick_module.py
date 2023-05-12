''' Joystick module '''
from typing import List
import pygame
from pygame.locals import *
from PyQt6.QtCore import pyqtSignal, QThread

class JoystickHandler(QThread):
    '''Joystick handler object'''
    change_pixmap_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.event.set_blocked((MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN))
        self.event_num = 0
        self.joystick_active = False
        self.joystick_id = 0
        self.joy = None
        self.name = ""
        self.num_axes    = 0
        self.num_balls   = 0
        self.num_buttons = 0
        self.num_hats    = 0
        self.available_joystick_list = []
        self.axis = []
        self.ball = []
        self.button = []
        self.hat = []
        self.refresh_joystick_list()

    # pylint: disable=R0801
    def get_joystick_list(self) -> List[str]:
        '''Return the list of Joysticks'''
        return self.available_joystick_list

    # pylint: disable=R0801
    def refresh_joystick_list(self) -> List[str]:
        '''Check pygame for available joysticks and info to create list'''
        self.joy_count = pygame.joystick.get_count()
        if self.joy_count == 0:
            print("This module requires at least one joystick plugged in.")
        arr = []

        for i in range(self.joy_count):
            self.joy = pygame.joystick.Joystick(i)
            arr.append(self.joy.get_name())

        self.available_joystick_list = arr
        return arr

    def set_joystick(self, joystick_id):
        '''Start getting actions from joystick'''
        if self.joystick_active:
            return

        self.joystick_id = joystick_id
        self.joy = pygame.joystick.Joystick(joystick_id)
        self.name = self.joy.get_name()
        self.joy.init()
        self.num_axes    = self.joy.get_numaxes()
        self.num_balls   = self.joy.get_numballs()
        self.num_buttons = self.joy.get_numbuttons()
        self.num_hats    = self.joy.get_numhats()

        self.axis = []
        for i in range(self.num_axes):
            self.axis.append(self.joy.get_axis(i))

        self.ball = []
        for i in range(self.num_balls):
            self.ball.append(self.joy.get_ball(i))

        self.button = []
        for i in range(self.num_buttons):
            self.button.append(self.joy.get_button(i))

        self.hat = []
        for i in range(self.num_hats):
            self.hat.append(self.joy.get_hat(i))

        self.joystick_active = True
        # spawn thread with callback signal

    def run(self):
        '''Run active joystick'''
        print(self.joy_count)
        if self.joy_count <= 0:
            return
        while self.joystick_active:
            # print("test")
            for event in [pygame.event.wait(), ] + pygame.event.get():
                if event.type == JOYAXISMOTION:
                    self.event_num = event.axis
                    self.axis[event.axis] = event.value
#                    self.change_pixmap_signal.emit({"EVENT": event.type, "axis" : event.axis, "value": event.value})
                    self.change_pixmap_signal.emit(event.type)
                elif event.type == JOYBALLMOTION:
                    self.event_num = event.ball
                    self.ball[event.ball] = event.rel
                    self.change_pixmap_signal(event.type)
#                    self.change_pixmap_signal.emit({"EVENT": event.type, "ball" : event.ball, "value": event.rel})
                elif event.type == JOYHATMOTION:
                    self.event_num = event.joy
                    self.joy[event.joy] = event.value
                    self.change_pixmap_signal.emit(event.type)
#                   self.change_pixmap_signal.emit({"EVENT": event.type, "joy" : event.joy, "value": event.value})
                elif event.type == JOYBUTTONUP:
                    self.event_num = event.button
                    self.button[event.button] = 0
                    self.change_pixmap_signal.emit(event.type)
#                    self.change_pixmap_signal.emit({"EVENT": event.type, "btn" : event.button, "value": 0})
                elif event.type == JOYBUTTONDOWN:
                    self.event_num = event.button
                    self.button[event.button] = 1
                    self.change_pixmap_signal.emit(event.type)
#                   self.change_pixmap_signal.emit({"EVENT": event.type, "btn" : event.button, "value": 1})

    # pylint: disable=R0801
    def stop(self):
        '''Sets run flag to False and waits for thread to finish'''
        self.joystick_active = False
        self.wait()
