'''The script for the driving loop'''
import time
from collections import deque
from typing import List
import cv2 as cv
from defines import States
from defines import ActionsDict
try:
    from computer_vision.driving.driving_states import DrivingStates
    from computer_vision.camera_handler.camera import Camera
    from computer_vision.car_communication.abstract_communication import AbstractCommunication
    from computer_vision.lib import display_arrow
except ImportError:
    from ..driving.driving_states import DrivingStates
    from camera_handler.camera import Camera
    from car_communication.abstract_communication import AbstractCommunication
    from ..lib import display_arrow

class SimulationAction: # pylint: disable=R0902
    '''The loop for driving'''
    def __init__(self, conf: dict,
                 driving: DrivingStates,
                 camera: Camera=None
                 ):
        self.conf = conf
        self.driving = driving
        self.camera = camera
        self.cur_action = None

        # ----- STATES ----- #
        self.state = States.DRIVING

        # ----- ACTION ----- #
        self.actions: List[ActionsDict] = deque()

        # ----- INIT ACTIONS ----- #
        if self.conf['simulation']['live'] is False:
            self.__init_actions()

    def __init_actions(self):
        frame = cv.imread(self.conf['simulation']['image_paths']['camera_view'])
        height, width, _ = frame.shape
        actions = self.driving.simulation(frame, (width, height))
        self.__update_actions(actions)

    def run(self):
        '''Method for running'''
        while True:
            actions = None
            if self.conf['simulation']['live']:
                actions = self.next() # pylint: disable=E1102
                if actions is not None:
                    self.actions = actions
            if self.actions is None or not self.actions:
                continue
            # pylint: disable=E1136
            if self.conf['simulation']['active']:
                self.cur_action = self.actions.popleft() if self.actions else None
            angle = self.cur_action['angle']
            speed = self.cur_action['speed']
            duration = self.cur_action['time']
            distance = speed * duration
            display_arrow(self.conf, angle, distance)

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
        if self.camera is None:
            return None
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