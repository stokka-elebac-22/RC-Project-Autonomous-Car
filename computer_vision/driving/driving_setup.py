'''The script for the driving loop'''
import os
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
    from computer_vision.camera_handler.lib import rotate_image
    from computer_vision.car_communication.abstract_communication import AbstractCommunication
except ImportError:
    from driving import Driving
    from camera_handler.camera import Camera
    from camera_handler.lib import rotate_image
    from car_communication.abstract_communication import AbstractCommunication

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

        # ----- TEXT ----- #
        self.image_attributes = {
            'image_paths': self.conf['simulation']['image_paths'],
            'org': (25, 50),
            'font': cv.FONT_HERSHEY_SIMPLEX,
            'font_scale': 1,
            'color': (70, 70, 255),
            'thickness': 1
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
            distance= speed * duration
            if self.conf['simulation']['live']:
                self.display(angle, distance)
            else:
                if self.previous['speed'] != speed and self.previous['angle'] != angle:
                    self.car_comm.drive_direction(speed, angle)
                    self.previous['speed'] = speed
                    self.previous['angle'] = angle
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
        match self.state:
            case States.WAITING:
                actions: List[ActionsDict] = self.driving.waiting(frame)
            case States.DRIVING:
                actions: List[ActionsDict] = \
                    self.driving.driving(frame, self.camera.get_dimensions())
            case States.STOPPING:
                actions: List[ActionsDict] = self.driving.stopping(frame)
            case States.PARKING:
                actions: List[ActionsDict] = \
                    self.driving.parking(frame, self.camera.get_dimensions())
        return actions

    def display(self, angle, distance) -> bool:
        '''Display the arrow or other symbols'''
        if angle is None or distance is None:
            return False
        distance = int(distance)
        arrow_image_path = self.image_attributes['image_paths']['arrow']
        if os.path.exists(arrow_image_path):
            img = cv.imread(arrow_image_path)
            img = rotate_image(img, angle) # rotate image
            img = cv.putText(
                img,
                f'Distance: {distance}',
                self.image_attributes['org'],
                self.image_attributes['font'],
                self.image_attributes['font_scale'],
                self.image_attributes['color'],
                self.image_attributes['thickness'],
                cv.LINE_AA)
            cv.imshow('', img)
            print(f'Move the car by {distance}mm at an angle of {angle} degrees.')
            cv.waitKey(0)
        else:
            print(f'Path does not exists: {self.image_paths["arrow"]}')
            raise FileNotFoundError
        return True
