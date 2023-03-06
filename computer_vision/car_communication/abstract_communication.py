#!/usr/bin/env python
"""AbstractCommunication.py: Abstract class describing communication."""

from abc import (ABC, abstractmethod,)

class AbstractCommunication(ABC):
    '''Abstract class for different communication types'''
    @abstractmethod
    def __init__(self, conn_info):
        pass

    @abstractmethod
    def start(self):
        ''' Establish connection '''

    @abstractmethod
    def stop(self):
        '''Stop serial connection'''

    @abstractmethod
    def send_command(self, command):
        '''Send command'''

    @abstractmethod
    def set_motor_speed(self, m0_dir: int, m0_speed: int, m1_dir: int, m1_speed):
        '''Set the motor speeds directly'''

    @abstractmethod
    def drive_direction(self, speed: int, angle: int):
        '''Depending on angle/speed make a calculation on motor speeds
        ### Should this be moved outside of the communication?'''

    @abstractmethod
    def get_next_data(self):
        '''Get next available piece of data'''
