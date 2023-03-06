#!/usr/bin/env python
"""abstract_storage.py: Class for handling CAN communication."""

import sqlite3

from abc import (ABC, abstractmethod,)

class AbstractStorage(ABC):
    '''Abstract class defining storage methods'''
    @abstractmethod
    def __init__(self, db_name: str):
        pass

    @abstractmethod
    def add_log(self, pos: int, sensor_type: int, value: int, timestamp=0):
        '''Add new sensor log'''

    @abstractmethod
    def create_project_tables(self):
        '''Create table/structure'''

    @abstractmethod
    def get_sensor_data(self, pos: int, sensor_type: int):
        '''Get sensor data from one sensor'''

    @abstractmethod
    def get_recent_sensor_data(self):
        '''Get most recent sensor data'''
