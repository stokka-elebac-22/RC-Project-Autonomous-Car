'''The script for the driving loop'''
import os
import sys
from collections import deque
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
    def __init__(self, conf: dict, driving: Driving, camera: Camera, image_paths: dict):
        self.conf = conf
        self.driving = driving
        self.camera = camera

        # ----- TEXT ----- #
        self.image_attributes = {
            'image_paths': image_paths,
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

    def run(self):
        '''Method for running'''
        while self.running:
            actions = self.next() # pylint: disable=E1102
            if actions is not None:
                self.__update_actions(actions)
            if self.actions is None or not self.actions:
                continue

            cur_action = self.actions.popleft()
            if cur_action is None:
                continue
            angle = cur_action['angle']
            speed = cur_action['speed']
            time = cur_action['time']
            distance= speed * time

            self.display(angle, distance)
        print('Stopping...')
        sys.exit()

    def __update_actions(self, actions) -> bool:
        '''Update actions'''
        if actions is None:
            return False
        angles = actions['angles']
        times = actions['times']
        self.actions: List[ActionsDict] = deque()
        for angle, time in zip(angles, times):
            self.actions.append({
                'speed': self.conf['spline']['velocity'],
                'angle': angle,
                'time': time,
            })
        return True

    def next(self) -> List[ActionsDict]:
        '''The next iteration in the loop'''
        ret, frame = self.camera.read()
        if not ret:
            return None
        if self.state == States.DRIVING:
            actions: List[ActionsDict] = self.driving.driving(frame, self.camera.get_dimensions())
        return actions

    def display(self, angle, distance) -> bool:
        '''Display the arrow or other symbols'''
        if angle is None or distance is None:
            return False
        arrow_image_path = self.image_attributes['image_paths']['arrow']
        if os.path.exists(arrow_image_path):
            img = cv.imread(arrow_image_path)
            img = rotate_image(img, angle*100) # rotate image
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
            cv.waitKey(0)
        else:
            print(f'Path does not exists: {self.image_paths["arrow"]}')
            raise FileNotFoundError
        return True
