'''The script for the driving loop'''
import sys
import time
from collections import deque
from typing import List
import cv2 as cv
from defines import States
from defines import ActionsDict
from pynput import keyboard
try:
    from computer_vision.driving.driving_states import Driving
    from computer_vision.camera_handler.camera import Camera
    from computer_vision.car_communication.abstract_communication import AbstractCommunication
    from computer_vision.lib import display_arrow
except ImportError:
    from driving import Driving
    from camera_handler.camera import Camera
    from car_communication.abstract_communication import AbstractCommunication
    from ..lib import display_arrow

class DrivingSetup:
    '''The loop for driving'''
    def __init__(self, conf: dict,
                 driving: Driving,
                 camera: Camera=None,
                 car_comm: AbstractCommunication= None):
        self.conf = conf
        self.driving = driving
        self.camera = camera
        self.car_comm = car_comm
        self.cur_action = None
        self.previous = {
            'angle': None,
            'speed': None,
            'time': time.time(),
        }

        # ----- STATES ----- #
        self.state = States.DRIVING

        # ----- ACTION ----- #
        self.actions: List[ActionsDict] = deque()

        # ----- INIT ACTIONS ----- #
        if self.conf['simulation']['live'] is False:
            self.__init_actions()

        # ----- INTERRUPTS ----- #
        self.running = True
        self.__interrupts()

    def __interrupts(self):
        '''Interrupts'''
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
        frame = cv.imread(self.conf['simulation']['image_paths']['camera_view'])
        height, width, _ = frame.shape
        actions = self.driving.driving(frame, (width, height))
        self.__update_actions(actions)

    def run(self):
        '''Method for running'''
        while self.running:
            actions = self.next() # pylint: disable=E1102
            if actions is not None:
                self.actions = actions
            if self.actions is None or not self.actions:
                continue
            time_now = self.previous['time'] - time.time()
            # pylint: disable=E1136
            if actions is not None or \
                (self.cur_action is not None and time_now >= self.cur_action['time']):
                self.cur_action = self.actions.popleft() if self.actions else None

            if self.cur_action is None or \
                (self.cur_action is not None and time_now >= self.cur_action['time']):
                angle = 0
                speed = 0
                duration = 0
            else:
                angle = self.cur_action['angle']
                speed = self.cur_action['speed']
                duration = self.cur_action['time']
            distance = speed * duration
            if self.conf['simulation']['live']:
                display_arrow(self.conf, angle, distance)
            else:
                if self.previous['speed'] != speed and self.previous['angle'] != angle:
                    self.car_comm.drive_direction(speed, angle)
                    self.previous['speed'] = speed
                    self.previous['angle'] = angle
                    self.previous['time'] = time.time()
        print('Stopping...')
        sys.exit()

    def __update_actions(self, actions) -> bool:
        '''Update actions'''
        if actions is None:
            return False
        angles = actions['angles']
        times = actions['times']
        self.actions: List[ActionsDict] = deque()
        for angle, duration in zip(angles, times):
            self.actions.append({
                'speed': self.driving.pathfinding.velocity,
                'angle': angle,
                'time': duration,
            })
        return True

    def next(self) -> List[ActionsDict]:
        '''The next iteration in the loop'''
        ret, frame = self.camera.read()
        if not ret:
            return None
        if self.state == States.WAITING:
            actions: List[ActionsDict] = self.driving.waiting(frame)
        elif self.state == States.DRIVING:
            actions: List[ActionsDict] = self.driving.driving(frame, self.camera.get_dimensions())
        elif self.state == States.STOPPING:
            actions: List[ActionsDict] = self.driving.stopping(frame)
        elif self.state == States.PARKING:
            actions: List[ActionsDict] = self.driving.parking(frame, self.camera.get_dimensions())
        return actions
